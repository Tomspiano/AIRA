from django.db import models

class airplane(models.Model):
    airplaneId = models.AutoField(primary_key=True)
    craftTypeCode = models.IntegerField(null=True)
    airlineName = models.CharField(max_length=20,null=True)
    craftType = models.CharField(max_length=10,null=True)

class flight(models.Model):
    flightId = models.AutoField(primary_key=True)
    flightNumber = models.CharField(max_length=20,null=True)
    dcityNum = models.CharField(max_length=20,null=True)
    acityNum = models.CharField(max_length=20,null=True)
    dcityName = models.CharField(max_length=20,null=True)
    acityName = models.CharField(max_length=20,null=True)
    departureTime = models.DateField(auto_now=False,null=True)
    arrivalTime = models.DateField(auto_now=False,null=True)
    departureAirportName = models.CharField(max_length=20,null=True)
    arrivalAirportName = models.CharField(max_length=20,null=True)

class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True)
    flightId = models.ForeignKey('flight',on_delete=models.CASCADE,null=True)
    airplaneId = models.ForeignKey('airplane',on_delete=models.CASCADE,null=True)
    companyId = models.ForeignKey('company',on_delete=models.CASCADE,null=True)
    price = models.IntegerField(null=True)
    dtime = models.TimeField(auto_now=False,null=True)
    atime = models.TimeField(auto_now=False,null=True)

class company(models.Model):
    companyId = models.AutoField(primary_key = True)
    company = models.CharField(max_length=20,null=True)
    site = models.URLField(null=True)
