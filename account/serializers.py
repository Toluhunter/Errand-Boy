from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

import numpy as np
import face_recognition


User = get_user_model()


class CreateAccountSerializer(serializers.ModelSerializer):

    '''
    Serializer to hanle account creation and enforcing strong password
    '''

    role = serializers.ChoiceField(choices=User.choices, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
        ]

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)

        self.fields["id"].read_only = True
        self.fields["password"].write_only = True

    def validate(self, attrs):
        # Checks password is strong enough using django's default password validators
        validate_password(attrs["password"])

        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        return user


class AccountSerializer(serializers.ModelSerializer):
    '''
    Serializer to handle fetching and updating of account details
    '''
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def __init__(self, instance=None, **kwargs) -> None:
        super().__init__(instance, **kwargs)
        self.fields["id"].read_only = True

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class ProfilePicSerializer(serializers.Serializer):
    '''
    For Review: Serializer to handle updating of profile picture
    '''
    profile_picture = serializers.ImageField()

    def create(self, validated_data):
        user = self.context["request"].user
        user.profile_picture = validated_data["profile_picture"]
        user.save()
        return user


class LoginSerializer(serializers.Serializer):

    '''
    Serializer to handle user login and retrival of refresh and access tokens
    '''

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        max_length=150, required=True, write_only=True)

    def validate(self, attrs):

        user = authenticate(
            username=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        refresh = RefreshToken.for_user(user=user)

        # Removes email and password details provided from the dictionary to be returned
        attrs.pop("email"),
        attrs.pop("password")
        # Adds refresh and access token values to the dictionary to be returned
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        for user_role, user_type in User.choices:
            '''
            loops over all user role value and string representation
            '''
            if user.role == user_role:
                # adds user role string representation to dictionary to be returned
                attrs["type"] = user_type

        return attrs


class RegisterFaceserializer(serializers.Serializer):
    '''
    Serializer to handle registration and validation of users face
    '''
    face = serializers.ImageField()

    def validate(self, attrs):
        # Reads face image (PNG, JPG, GIF) then returns numpy array
        image = face_recognition.load_image_file(attrs["face"])
        # extracts 128-dimensional face encoding for each face detected returns nothing if no valid face
        face_encoding = face_recognition.face_encodings(image)
        if not face_encoding:
            raise serializers.ValidationError("Invalid Face")

        return attrs

    def create(self, validated_data):

        user = self.context["request"].user
        user.face = validated_data["face"]
        user.save()

        return user


class FaceRecognitionLoginSerializer(serializers.Serializer):

    face = serializers.ImageField()
    email = serializers.EmailField()

    def validate(self, attrs):
        user = None
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid Credentials")

        # Reads face image (PNG, JPG, GIF) then returns numpy array
        image = face_recognition.load_image_file(user.face)
        # extracts first 128-dimensional face encoding from list of each face detected returns nothing if no valid face
        verified_face_encoding = face_recognition.face_encodings(image)[0]

        image = face_recognition.load_image_file(attrs["face"])
        # extracts 128-dimensional face encoding for each face detected returns nothing if no valid face
        face_encodings = face_recognition.face_encodings(image)
        if not face_encodings:
            raise serializers.ValidationError("Invalid Face")

        # compares face encodings received with users face
        matches = face_recognition.compare_faces(
            face_encodings, verified_face_encoding)

        face_distances = face_recognition.face_distance(
            face_encodings, verified_face_encoding)
        best_match_index = np.argmin(face_distances)

        if not matches[best_match_index]:
            raise serializers.ValidationError("Face Not Recognized")

        refresh = RefreshToken.for_user(user=user)

        # Removes email and password details provided from the dictionary to be returned
        attrs.pop("email")
        attrs.pop("face")
        # Adds refresh and access token values to the dictionary to be returned
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        for user_role, user_type in User.choices:
            '''
            loops over all user role value and string representation
            '''
            if user.role == user_role:
                # adds user role string representation to dictionary to be returned
                attrs["type"] = user_type

        return attrs


class RefreshAccessSerializer(serializers.Serializer):
    '''
    Return new refresh and access token, and blacklist old refresh token
    '''
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):

        refresh = RefreshToken(attrs["refresh"])
        refresh.verify()

        # Blacklist token id
        refresh.blacklist()

        # generate new exp, issued date and id for token to be sent back
        refresh.set_exp()
        refresh.set_iat()
        refresh.set_jti()

        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)

        return attrs


class LogoutSerializer(serializers.Serializer):
    '''
    Serializer to Logout User
    '''

    refresh = serializers.CharField(required=True)

    def validate(self, attrs):

        refresh = attrs["refresh"]

        try:
            refresh = RefreshToken(refresh)
            refresh.verify()
        except TokenError as e:
            raise serializers.ValidationError(e)

        refresh.blacklist()

        return attrs
