from rest_framework import serializers
from chairsapp.models import Order  # Import the Order model

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Include all fields from the Order model
