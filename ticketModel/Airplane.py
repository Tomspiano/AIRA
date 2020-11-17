from django.db import models

class Airplane(models.Model):
    airplaneNumber = models.CharField(primary_key=True, max_length=20)
    craftTypeCode = models.IntegerField()
    airlineName = models.CharField(max_length=20)
    craftType = models.CharField(max_length=10)

class Flight(models.Model):
    flightNumber = models.CharField(primary_key=True, max_length=20)
    departureCity = models.CharField(max_length=20)
    arrivalCity = models.CharField(max_length=20)
    departureTime = models.DateTimeField(auto_now=False,null=True)
    arrivalTime = models.DateTimeField(auto_now=False,null=True)
    departureAirportName = models.CharField(max_length=20)
    arrivalAirportName = models.CharField(max_length=20)

class Ticket(models.Model):
    flightNumber = models.ForeignKey('Flight',on_delete=models.CASCADE)
    airplaneNumber = models.ForeignKey('Airplane',on_delete=models.CASCADE)
    company = models.CharField(max_length=20)
    price = models.IntegerField()
    ticketType = models.CharField(max_length=20)
    returnRule = models.CharField(max_length=100)

class Company(models.Model):
    company = models.CharField(max_length=20)
    site = models.URLField()
