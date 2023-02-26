from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class CreateAccountSerializer(serializers.ModelSerializer):

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
        validate_password(attrs["password"])

        return attrs
    
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        return user
    

class AccountSerializer(serializers.ModelSerializer):
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

    profile_picture = serializers.ImageField()

    def create(self, validated_data):
        
        user = self.context["request"].user

        user.profile_picture = validated_data["profile_picture"]

        user.save()

        return user

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, write_only = True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)

    def validate(self, attrs):
        
        user = authenticate(username=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        refresh = RefreshToken.for_user(user=user)

        attrs.pop("email"),
        attrs.pop("password")
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        for user_role, user_type in User.choices:
            if user.role == user_role:
                attrs["type"] = user_type

        return attrs

class RefreshAccessSerializer(serializers.Serializer):

    refresh = serializers.CharField(required=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):

        refresh = RefreshToken(attrs["refresh"])
        refresh.verify()
        refresh.blacklist()

        refresh.set_exp()
        refresh.set_iat()
        refresh.set_jti()

        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)

        return attrs

class LogoutSerializer(serializers.Serializer):

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
        