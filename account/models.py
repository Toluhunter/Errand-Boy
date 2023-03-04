import os
from uuid import uuid4

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from .validators import phonenumber_validators


class UserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):

        user = self.model(**other_fields)
        user.set_password(password)
        user.email = self.normalize_email(email)

        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault("is_active", True)

        return self.create_user(email=email, password=password, )


class Account(AbstractBaseUser, PermissionsMixin):

    def upload_face_image(model, filename):
        extension = filename.split(".")[-1]
        return os.path.join("auth", model.email, f"face.{extension}")

    USER = 3
    COURIER = 2
    FOODPROVIDER = 1

    choices = [
        (USER, "User"),
        (COURIER, "Courier"),
        (FOODPROVIDER, "FoodProvider")
    ]
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(default=uuid4, null=False,
                          blank=False, primary_key=True, unique=True)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False)
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False)
    email = models.EmailField(
        _("email address"), blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=14, null=False, blank=False, validators=[
                                    phonenumber_validators], unique=True)
    face = models.ImageField(null=True, blank=True,
                             upload_to=upload_face_image)
    role = models.PositiveSmallIntegerField(
        choices=choices, default=USER, null=False, blank=False)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    authenticationmodel = models.BinaryField(blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def generate_id(self):
        id = uuid4()

        while (Account.objects.filter(id=id).exists()):
            id = uuid4()

        return id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()

        self.full_clean()
        return super().save(*args, **kwargs)
