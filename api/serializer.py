from rest_framework import serializers
from .models import notes


class noteSerializer(serializers.ModelSerializer):
    class Meta:
        model = notes
        fields = ['id', 'title', 'desc', 'image', 'status']