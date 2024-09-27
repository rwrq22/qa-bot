from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from chat_rooms.models import ChatRoom

# from .models import ChatResponse
from .serializers import MessageSerializer

from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)


class Messages(APIView):
    def get(self, request):  # session key 확인 후 데이터 가져옵니다
        session_key = request.session.session_key
        if not session_key:
            return Response(
                {"error": "Session does not exist."}, status=HTTP_400_BAD_REQUEST
            )
        chat_room = ChatRoom.objects.get(session_key=session_key)
        all_messages = Message.objects.filter(chat_room=chat_room)
        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        chat_room = ChatRoom.objects.get(session_key=session_key)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            new_message = serializer.save(chat_room=chat_room)
            return Response(MessageSerializer(new_message).data)

    def delete(self, request):
        all_messages = Message.objects.all()
        all_messages.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    authentication_classes = []
