from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message

# from .models import ChatResponse
from .serializers import MessageSerializer
from inputs.serializers import InputSerializer

from rest_framework.status import HTTP_204_NO_CONTENT


class Messages(APIView):
    def get(self, request):
        all_messages = Message.objects.all()
        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            new_message = serializer.save()
            input_serializer = InputSerializer(data={"text": new_message.response})
            if input_serializer.is_valid():
                new_input = input_serializer.save()
            return Response(MessageSerializer(new_message).data)

    def delete(self, request):
        all_messages = Message.objects.all()
        all_messages.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    authentication_classes = []
