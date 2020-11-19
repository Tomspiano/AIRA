from rest_framework import serializers
from . import models

class ticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        field = '__all__'

class airplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.airplane
        field = '__all__'

class flightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.flight
        field = '__all__'

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.company
        field = '__all__'