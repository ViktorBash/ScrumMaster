from .models import Board, SharedUser, Task
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import BoardCreateSerializer, BoardInfoSerializer


# Create a board, POST request, requires authentication, returns board info
class BoardCreate(generics.GenericAPIView):
    serializer_class = BoardCreateSerializer
    # authentication_classes = (TokenAuthentication,)
    # The request must be authenticated to access the API
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # POST request part
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Check serializer is valid, then save it if it is
        board = serializer.save()

        # Return info about the board using the BoardInfoSerializer
        return Response({
            "board": BoardInfoSerializer(board, context=self.get_serializer_context()).data
        })
