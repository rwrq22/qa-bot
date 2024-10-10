# Third party packages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

# Django applications
from .models import Message
from chat_rooms.models import ChatRoom

# Other custom applications
from .serializers import MessageSerializer


class Messages(APIView):
    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):  # session key 확인 후 데이터 가져옵니다
        session_key = request.session.session_key
        chat_room = ChatRoom.objects.get(session_key=session_key)
        all_messages = Message.objects.filter(chat_room=chat_room)
        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            session_key = request.session.session_key
            chat_room = ChatRoom.objects.get(session_key=session_key)
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                new_message = serializer.save(chat_room=chat_room)
                return Response(MessageSerializer(new_message).data)
        except Exception as e:
            return Response(Response({"error": e}, status=HTTP_400_BAD_REQUEST))

    def delete(self, request):
        all_messages = Message.objects.all()
        all_messages.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    authentication_classes = []
