from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import ChatRoom
from .serializers import ChatRoomSerializer


class ChatRooms(APIView):
    def get_session_key(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return session_key

    def get(self, request):
        session_key = self.get_session_key(request)
        try:
            chat_room = ChatRoom.objects.get(session_key=session_key)
        except ChatRoom.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        try:
            session_key = self.get_session_key(request)
            serializer = ChatRoomSerializer(data=request.data)
            if serializer.is_valid():
                new_chat_room = serializer.save(session_key=session_key)
                return Response(ChatRoomSerializer(new_chat_room).data)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            session_key = self.get_session_key(request)
            chat_room = ChatRoom.objects.get(session_key=session_key)
            chat_room.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


def trigger_error(request):
    division_by_zero = 1 / 0
