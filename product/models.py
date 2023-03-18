from uuid import uuid4
from random import randint

from django.db import models
from django.core.validators import MinValueValidator
from foodservice.models import FoodService


class Category(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=60, null=False, blank=False)
    foodservice = models.ForeignKey(
        to=FoodService, null=False, blank=False, on_delete=models.CASCADE)


def set_id():
    return randint(int('1'*15), int('9' * 15))


class Product(models.Model):

    id = models.BigIntegerField(default=set_id, primary_key=True)
    product_id = models.CharField(
        max_length=75, unique=True, blank=False, null=False)
    name = models.CharField(max_length=60, null=False, blank=False)
    price = models.FloatField(null=False, blank=False, validators=[
                              MinValueValidator(0.0)])
    image = models.ImageField(null=False, blank=False)
    foodservice = models.ForeignKey(
        to=FoodService, null=False, blank=False, on_delete=models.CASCADE)
    category = models.ForeignKey(
        to=Category, null=True, blank=False, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("name", "foodservice")

    def set_product_id(self):
        '''
        Generate user friendly id for product with use of title and product's id
        '''
        name = self.name.lower().replace(" ", "-")
        return f'{name}-{self.id}'

    def __str__(self):
        return f'{self.foodservice} {self.name}'

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = self.set_product_id()

        self.full_clean()

        return super().save(*args, **kwargs)
