from rest_framework import serializers
from .models import Suite
from rest_framework.decorators import api_view

class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = '__all__'
