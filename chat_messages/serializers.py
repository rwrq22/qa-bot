from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "pk",
            "question",
            "response",
        )
        read_only_fields = ["chat_room", "response"]
