from django.db import models

class Tickets(models.Model):
    departureDate = models.DateTimeField
    arrivalDate = models.DateTimeField
    flightNumber = models.CharField(max_length=20)
    dcity = models.CharField(max_length=20)
    acity = models.CharField(max_length=20)
    price = models.SmallIntegerField
    rate = models.FloatField
    url = models.CharField(max_length=150)
# Create your models here.