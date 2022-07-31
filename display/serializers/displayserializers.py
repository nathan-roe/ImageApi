from rest_framework import serializers
from display.models.display import Display


class DisplayAllSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Display objects with all fields returned
    """
    class Meta:
        model = Display
        fields = '__all__'
