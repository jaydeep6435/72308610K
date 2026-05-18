from rest_framework import serializers
from .vehicle_serializer import VehicleTaskSerializer

class OptimizationResponseSerializer(serializers.Serializer):
    """Serializer for the final Schedule Optimization Response"""
    depotId = serializers.IntegerField(required=True)
    availableHours = serializers.IntegerField(required=True, min_value=0)
    usedHours = serializers.IntegerField(required=True, min_value=0)
    remainingHours = serializers.IntegerField(required=True, min_value=0)
    totalImpact = serializers.IntegerField(required=True, min_value=0)
    selectedTasks = VehicleTaskSerializer(many=True, required=True)
