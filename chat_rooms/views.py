from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from .models import ChatRoom
from .serializers import ChatRoomSerializer


class ChatRooms(APIView):
    def get(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        try:
            chat_room = ChatRoom.objects.get(session_key=session_key)
        except ChatRoom.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            new_chat_room = serializer.save(session_key=session_key)
            return Response(ChatRoomSerializer(new_chat_room).data)

    def delete(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        chat_room = ChatRoom.objects.get(session_key=session_key)
        chat_room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
