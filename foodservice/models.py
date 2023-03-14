import os
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


def handle_store_picture(model, filename: str):

    extension = filename.split(".")[-1]
    return f"{model.name}{os.sep}{model.name}-store.{extension}"


class FoodService(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.OneToOneField(
        on_delete=models.CASCADE, to=User, null=False, blank=False, related_name="foodservice")
    name = models.CharField(max_length=40, null=False,
                            blank=False, unique=True)
    store_picture = models.FileField(
        null=False, blank=False, upload_to=handle_store_picture)
    location = models.TextField(null=False, blank=False)
    opening_time = models.TimeField(null=False, blank=False)
    closing_time = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.name
