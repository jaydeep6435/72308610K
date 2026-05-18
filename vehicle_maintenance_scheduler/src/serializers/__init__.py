# Expose all serializers through the package root for clean imports
from .depot_serializer import DepotSerializer
from .vehicle_serializer import VehicleTaskSerializer
from .optimization_serializer import OptimizationResponseSerializer
from .notification_serializer import NotificationSerializer

__all__ = [
    "DepotSerializer",
    "VehicleTaskSerializer",
    "OptimizationResponseSerializer",
    "NotificationSerializer"
]
