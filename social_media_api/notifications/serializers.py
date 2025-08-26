from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'is_read', 'timestamp']
        read_only_fields = ['recipient', 'actor', 'verb', 'target', 'timestamp']
