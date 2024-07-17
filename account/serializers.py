from rest_framework import serializers
from .models import Bill, Users

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'name_of_item', 'description', 'price', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'username', 'password']