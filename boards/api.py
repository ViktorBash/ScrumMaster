from .models import Board, SharedUser, Task
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import BoardCreateSerializer, BoardInfoSerializer, SharedUserCreateSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework import exceptions


# Create a board, POST request, requires authentication, returns board info
class BoardCreate(generics.GenericAPIView):
    serializer_class = BoardCreateSerializer
    # authentication_classes = (TokenAuthentication,)
    # The request must be authenticated to access the API
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # POST request to create Board
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Check serializer is valid, then save it if it is
        board = serializer.save()

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
            # Return 404 error
            raise exceptions.NotFound

        # If either board owner or shared user give board info, otherwise return 404 error that board does not exist
        if board.owner == self.request.user:
            pass
        else:
            try:
                SharedUser.objects.get(shared_user=self.request.user, board=board)
            except Exception:  # No shared user or board owner object exists, 404 response back
                raise exceptions.NotFound
        serializer = BoardInfoSerializer(board, many=False)
        return JsonResponse(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception:
            raise exceptions.NotFound
        if self.request.user == board.owner:
            board.delete()
            return JsonResponse("", safe=False)  # Return blank 200 response, successfully deleted
        else:  # Not owner of board, send 404
            raise exceptions.NotFound

    def put(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception:  # 404, doesn't exist
            return exceptions.NotFound
        if board.owner == self.request.user:
            serializer = BoardInfoSerializer(board, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:  # Not owner, 404 for security
            raise exceptions.NotFound


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


# Create shared user
class SharedUserCreate(generics.GenericAPIView):
    serializer_class = SharedUserCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_user = serializer.save()
        # return JsonResponse(shared_user, safe=False)
        return JsonResponse("lol", safe=False)

