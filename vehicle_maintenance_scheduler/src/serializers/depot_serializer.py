from rest_framework import serializers

class DepotSerializer(serializers.Serializer):
    """Serializer for Depot entity"""
    depotId = serializers.IntegerField(required=True)
    availableHours = serializers.IntegerField(required=True, min_value=0)
