from django.contrib.auth.models import User
from django.db import models


class HatOrder(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10)

    WOOL = "wool"
    FELT = "felt"
    MATERIAL_CHOICES = [
        (WOOL, "Wool"),
        (FELT, "Felt"),
    ]
    material = models.CharField(max_length=10, choices=MATERIAL_CHOICES, default=WOOL)

    order_number = models.IntegerField()
    """The customer's reference for the order"""
