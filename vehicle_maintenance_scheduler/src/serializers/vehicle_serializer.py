from rest_framework import serializers

class VehicleTaskSerializer(serializers.Serializer):
    """Serializer for individual Vehicle Maintenance Task"""
    TaskID = serializers.CharField(required=True, max_length=255)
    Duration = serializers.IntegerField(required=True, min_value=1)
    Impact = serializers.IntegerField(required=True, min_value=1)
