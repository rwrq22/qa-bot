from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Input
from .serializers import InputSerializer
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound


class Inputs(APIView):
    def get(self, request):
        all_inputs = Input.objects.all()
        serializer = InputSerializer(all_inputs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            new_input = serializer.save()
            return Response(InputSerializer(new_input).data)

    def delete(self, request):
        all_inputs = Input.objects.all()
        all_inputs.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    authentication_classes = []
