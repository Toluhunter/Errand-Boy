from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)
    # foodservice = models.ForeignKey()