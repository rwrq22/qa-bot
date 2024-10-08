from rest_framework import serializers
from .models import ChatRoom
from chat_messages.serializers import MessageSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    session_key = serializers.CharField(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ("pk", "session_key", "messages")
