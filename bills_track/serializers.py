from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'name_of_item', 'description', 'price', 'created_at']