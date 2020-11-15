from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    # departureDate = serializers.DateTimeField(auto_now=False, null=True)
    # arrivalDate = serializers.DateTimeField(auto_now=False, null=True)
    # flightNumber = serializers.CharField(max_length=20)
    # dcity = serializers.CharField(max_length=20)
    # acity = serializers.CharField(max_length=20)
    # price = serializers.IntegerField(null=True)
    # rate = serializers.FloatField(null=True)
    # url = serializers.CharField(max_length=150)
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        # instance.departureDate = validated_data.get('departureDate',instance.departureDate)
        # instance.arrivalDate = validated_data.get('arrivalDate',instance.arrivalDate)
        # instance.flightNumber = validated_data.get('flightNumber',instance.flightNumber)
        # instance.dcity = validated_data.get('dcity',instance.dcity)
        # instance.acity = validated_data.get('acity',instance.acity)
        # instance.price = validated_data.get('price',instance.price)
        # instance.rate = validated_data.get('rate',instance.rate)
        # instance.url = validated_data.get('url',instance.url)
        ticket = self.context['request'].ticket

        instance.sava()
        return instance