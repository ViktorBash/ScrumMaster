from .models import Board, SharedUser, Task
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import BoardCreateSerializer, BoardInfoSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


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
        if isinstance(board, str):
            return Response({
                "board": board
            })

        # Return info about the board using the BoardInfoSerializer
        return Response({
            "board": BoardInfoSerializer(board, context=self.get_serializer_context()).data
        })


# Gives info about a board when given ID
class BoardInfo(generics.GenericAPIView):
    serializer_class = BoardInfoSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    # GET request with PK/ID passed in the URL
    def get(self, request, pk, *args, **kwargs):
        # Try to get the board based on the ID and raise error if does not exist
        try:
            board = Board.objects.get(id=pk)
        except Exception as e:
            # Return Exception as JSON
            return JsonResponse(str(e), safe=False)

        # Check that the user either owns the board or is a shared user on it
        # set permission_allowed to true if either the owner or a shared user of the board
        permission_allowed = False
        if board.owner == self.request.user:
            permission_allowed = True
        else:
            try:
                SharedUser.objects.get(shared_user=self.request.user, board=board)
                permission_allowed = True
            except Exception:
                pass

        if permission_allowed:  # They have access to the board, give the board response
            # Put the board in the serializer and return it as a JSON response.
            serializer = BoardInfoSerializer(board, many=False)
            return JsonResponse(serializer.data)
        else:  # They don't have permission, deny them
            return JsonResponse("Permission denied", safe=False)

    def delete(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception as e:
            return JsonResponse(str(e), safe=False)
        if self.request.user == board.owner:
            board.delete()
            return JsonResponse("board deleted", safe=False)
        else:
            return Response("Incorrect Credentials")

    def put(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception as e:
            return JsonResponse(str(e), safe=False)
        if board.owner == self.request.user:
            serializer = BoardInfoSerializer(board, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response("Incorrect Credentials")


# List the boards GET request, shows owned and shared boards
class BoardList(generics.GenericAPIView):
    serializer_class = BoardInfoSerializer
    permission_classes = [  # Have to be authenticated
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        owned_boards = self.request.user.board.all()  # Get all of the boards the user owns
        shared_user_objects = self.request.user.shared_boards.all()  # get all of the shared user objects that belong to
        # the user
        # this comprehension turns the shared user objects into a list of the boards the user is shared to
        shared_boards_list = [shared_user_object.board for shared_user_object in shared_user_objects]
        owned_serializer = BoardInfoSerializer(owned_boards, many=True)  # serialize the boards owned
        shared_serializer = BoardInfoSerializer(shared_boards_list, many=True)  # serialize the boards shared to
        # send both the shared and owned boards as JSON back
        return JsonResponse(owned_serializer.data + shared_serializer.data, safe=False)


