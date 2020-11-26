from rest_framework import serializers
from . import models


class airplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.airplane
        fields = '__all__'

class flightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.flight
        fields = '__all__'

class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.company
        fields = '__all__'

class ticketSerializer(serializers.ModelSerializer):
    airplane = airplaneSerializer()
    class Meta:
        model = models.Ticket
        fields = '__all__'
