from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    """Serializer for outgoing Notification payloads"""
    message = serializers.CharField(required=True, max_length=1000)
    recipient = serializers.EmailField(required=True)
    status = serializers.CharField(required=False, max_length=50)
