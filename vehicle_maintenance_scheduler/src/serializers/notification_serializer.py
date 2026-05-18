from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    """Enhanced Serializer for outgoing Notification payloads"""
    type = serializers.ChoiceField(choices=["Placement", "Result", "Event"], required=True)
    message = serializers.CharField(required=True, max_length=1000)
    recipient = serializers.EmailField(required=True)
    status = serializers.CharField(required=False, max_length=50)
    timestamp = serializers.DateTimeField(required=False)

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value
