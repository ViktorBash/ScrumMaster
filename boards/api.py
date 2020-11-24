from .models import Board, SharedUser, Task
from rest_framework.response import Response
from rest_framework import generics, permissions
from .serializers import BoardCreateSerializer, BoardInfoSerializer, SharedUserCreateSerializer, \
    SharedUserDeleteSerializer, TaskSerializer, BoardUpdateSerializer, BoardListSerializer
from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework import status

"""
All api views required permissions.IsAuthenticated to ensure there is a user sending a request.
Otherwise, serializers and other pieces of the code will not function correctly.
Most error responses are exceptions.NotFound (aka 404). Even if an object exists but the user is not allowed to view it,
a 404 is still given for security purposes.
Most API views have multiple checks (or their serializers do), in order to check that the object exists, they are either
an owner os have access to the object, etc.


One object can have up to 3 different api views:
ObjectCreate --> API view for POST
ObjectInfo --> API view for GET, PUT and DELETE
ObjectList --> API view for GET request for a list of the objects
"""


# Create a board, POST request, requires authentication, returns board info
class BoardCreate(generics.GenericAPIView):
    serializer_class = BoardCreateSerializer
    # The request must be authenticated to access the API
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # POST request to create Board
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Check serializer is valid, then save the board if it is
        board = serializer.save()

        # Return info about the board using the BoardInfoSerializer
        return JsonResponse(
            BoardInfoSerializer(board.id).data, status=status.HTTP_201_CREATED
        )


# Gives board info and related tasks when given ID
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
        except Exception:
            raise exceptions.NotFound

        # If either board owner or shared user give board info, otherwise return 404 error that board does not exist
        if board.owner == self.request.user:
            pass
        else:
            try:
                SharedUser.objects.get(shared_user=self.request.user, board=board)
            except Exception:  # No shared user or board owner object exists, 404 response back
                raise exceptions.NotFound

        board_serializer = BoardInfoSerializer(pk, many=False)
        return JsonResponse(board_serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception:
            raise exceptions.NotFound
        if self.request.user == board.owner:
            board.delete()
            return Response(status=status.HTTP_200_OK)  # Return blank 200 response, successfully deleted
        else:  # Not owner of board, send 404
            raise exceptions.NotFound

    def put(self, request, pk, *args, **kwargs):
        try:
            board = Board.objects.get(id=pk)
        except Exception:  # 404, doesn't exist
            raise exceptions.NotFound

        if board.owner == self.request.user:
            serializer = BoardUpdateSerializer(board, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:  # Not owner, 404 for security
            raise exceptions.NotFound


# List the boards, GET request, shows owned and shared boards
class BoardList(generics.GenericAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        # Get the user id, put it into the serializer. Then return the serializer data.
        user_id = self.request.user.id
        serializer = BoardListSerializer(user_id)
        return JsonResponse(serializer.data)


# Create shared user
class SharedUserCreate(generics.GenericAPIView):
    serializer_class = SharedUserCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_user = serializer.save()
        return Response(shared_user, status=status.HTTP_201_CREATED)


# Delete shared user
class SharedUserDelete(generics.GenericAPIView):
    serializer_class = SharedUserDeleteSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK)


# Task Create API View
class TaskCreate(generics.GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Check serializer is valid, then save it if it is
        task = serializer.save()
        return_response = {
            "task": {
                "id": task.id,
                "board": task.board.id,
                "date_created": task.date_created,
                "title": task.title,
                "description": task.description,
                "progress_status": task.progress_status,
                "priority": task.priority,
                "owner": {
                    "username": task.owner.username,
                    "first_name": task.owner.first_name,
                    "last_name": task.owner.last_name,
                    "email": task.owner.email,
                }
            }
        }
        return JsonResponse(return_response, safe=False)


# Task info (update, delete) API view
class TaskInfo(generics.GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # TaskInfo GET request API endpoint removed (just use BoardInfo for data on the board and accompanying Tasks)
    # def get(self, request, pk, *args, **kwargs):
    #     try:
    #         task = Task.objects.get(id=pk)
    #     except Exception:
    #         raise exceptions.NotFound
    #
    #     allowed = False
    #     board = task.board
    #     if self.request.user == board.owner:
    #         allowed = True
    #     else:
    #         try:
    #             shared_user = board.shared_users.get(board=board, shared_user=self.request.user)
    #             allowed = True
    #         except Exception:
    #             raise exceptions.NotFound
    #
    #     if not allowed:
    #         return exceptions.NotFound
    #
    #     return_response = {
    #         "task": {
    #             "id": task.id,
    #             "board": task.board.id,
    #             "date_created": task.date_created,
    #             "title": task.title,
    #             "description": task.description,
    #             "progress_status": task.progress_status,
    #             "priority": task.priority,
    #             "owner": {
    #                 "username": task.owner.username,
    #                 "first_name": task.owner.first_name,
    #                 "last_name": task.owner.last_name,
    #                 "email": task.owner.email,
    #             }
    #         }
    #     }
    #     return JsonResponse(return_response, safe=False)

    def put(self, request, pk, *args, **kwargs):
        try:
            task = Task.objects.get(id=pk)
        except Exception:
            raise exceptions.NotFound

        allowed = False
        board = task.board

        if board.owner == self.request.user:
            allowed = True
        else:
            try:
                shared_user = board.shared_users.get(board=board, shared_user=self.request.user)
                allowed = True
            except Exception:
                raise exceptions.NotFound

        if not allowed:
            raise exceptions.NotFound

        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return_response = {
            "task": {
                "id": task.id,
                "board": task.board.id,
                "date_created": task.date_created,
                "title": task.title,
                "description": task.description,
                "progress_status": task.progress_status,
                "priority": task.priority,
                "owner": {
                    "username": task.owner.username,
                    "first_name": task.owner.first_name,
                    "last_name": task.owner.last_name,
                    "email": task.owner.email,
                }
            }
        }
        return JsonResponse(return_response, safe=False)

    def delete(self, request, pk, *args, **kwargs):
        try:
            task = Task.objects.get(id=pk)
        except Exception:
            raise exceptions.NotFound

        allowed = False
        board = task.board

        if board.owner == self.request.user:
            allowed = True
        else:
            try:
                shared_user = board.shared_users.get(board=board, shared_user=self.request.user)
                allowed = True
            except Exception:
                raise exceptions.NotFound

        if not allowed:
            raise exceptions.NotFound

        task.delete()
        return Response(status=status.HTTP_200_OK)

