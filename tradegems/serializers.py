from rest_framework import serializers
from .models import *

class CustomersSerializer(serializers.ModelSerializer):
    gem = serializers.StringRelatedField(many=True)
    class Meta():
        model = Customer
        fields = ['username','spent_money','gem']

class TradeGemsSerializer(serializers.ModelSerializer):
    class Meta():
        model = UploadFile
        fields = ['deals']
