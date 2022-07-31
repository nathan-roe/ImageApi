from rest_framework import serializers
from util.models.tokens import ExpiringToken


class ExpiringTokenAllSerializer(serializers.ModelSerializer):
    """
    Serializer for handling ExpiringToken objects with all fields returned
    """
    class Meta:
        model = ExpiringToken
        fields = '__all__'
