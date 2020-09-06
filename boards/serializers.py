from rest_framework import serializers
from .models import Board, SharedUser, Task
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework import exceptions

"""
Serializers for API.
Most serializers check multiple things such as if user exists, if user has access to the object, if the object exists,
etc. After that the object is usually saved or deleted.
"""


# Board create serializer for POST requests
class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        # Only the "title" field will be writable
        model = Board
        fields = ['title', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):  # POST request
        # Gets user object from response, no user = validation error (there should be a user though, just another layer
        # of protection).
        owner = None
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            owner = request.user
        if owner is None:
            raise serializers.ValidationError("Incorrect Credentials")

        # Create the board with the given title and the owner who sent the request
        board = Board(title=validated_data['title'], owner=owner)
        try:
            board.save()  # Save to model
        except IntegrityError:  # Integrity error if the user already has a board with this name, since name is
            # unique for every owner in the Board model
            error_dict = {"title": ["You already have a board with this title."]}
            raise serializers.ValidationError(error_dict)
        return board  # Return board object if save is successful


# Serializer for GET, PUT and DELETE requests for board object.
class BoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']  # Read only, title is only thing that can be updated


# Shared User serializer for POST (create)
class SharedUserCreateSerializer(serializers.Serializer):
    # to create all we need is a board id and the email of the shared user.
    board_id = serializers.IntegerField()
    shared_user_email = serializers.EmailField()

    def create(self, validated_data):  # POST request
        # Check if board exists
        try:
            board = Board.objects.get(id=validated_data['board_id'])
        except Exception:
            raise exceptions.NotFound

        # Check if there is a user (should be, just another layer of protection), and if the user is
        # the owner of the board
        owner = None
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            owner = request.user
        if owner is None or board.owner != owner:
            raise exceptions.NotFound

        # Check if the user who we want to add exists
        try:
            user = User.objects.get(email=validated_data['shared_user_email'])
        except Exception:
            raise exceptions.NotFound("No user with that email")

        # See if the shared_user already exists. If it is, we raise a validation error
        check_shared_user = None
        try:
            check_shared_user = SharedUser.objects.get(board=board, shared_user=user)
        except Exception:
            pass
        if check_shared_user:
            raise exceptions.ValidationError({"detail": "This user is already added to the board"})

        # Passed all tests, put it together, create the shared user
        shared_user = SharedUser.objects.create(board=board, shared_user=user)
        shared_user.save()
        return_info = {
            "shared_user": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "board_id": board.id
        }
        return return_info


# For GET requests
class SharedUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedUser
        fields = ['board', 'shared_user']
        read_only_fields = ['board', 'shared_user']


# To delete a shared user
class SharedUserDeleteSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    shared_user_email = serializers.EmailField()

    def create(self, validated_data):  # Actually a DELETE request
        # Check if shared_user exists
        try:
            print(validated_data)
            user = User.objects.get(email=validated_data['shared_user_email'])
            shared_user = SharedUser.objects.get(board_id=validated_data['board_id'], shared_user=user)
        except Exception as e:
            raise exceptions.NotFound("Shared user not found")

        # Check if owner of the board
        board = Board.objects.get(id=validated_data['board_id'])  # already checked that board exists above
        owner = None
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            owner = request.user
        if owner is None or board.owner != owner:
            raise exceptions.NotFound

        # Passed shared user exists and is board owner checks. Delete the shared user now and return "".
        shared_user.delete()
        return ""


# Task serializer for POST, PUT, DELETE. GET does not use serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'board', 'date_created', 'title', 'description', 'progress_status', 'priority', 'owner']
        read_only_fields = ['id', 'date_created']

    def create(self, validated_data):
        # Get the user or raise an error
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user is None:
            raise serializers.ValidationError("Incorrect Credentials")

        # Try to get the board
        try:
            board = Board.objects.get(id=validated_data['board'].id)
        except Exception:
            raise exceptions.NotFound

        # see if they have access to the board (if they are owner or shared user)
        allowed = False
        if user.id is board.owner.id:
            allowed = True
        else:
            try:
                user = board.shared_users.get(board=board, shared_user=user)
                allowed = True
            except Exception as e:
                raise exceptions.NotFound
        if allowed is False:
            raise serializers.ValidationError("Incorrect Credentials")

        # Create the task

        task = Task(title=validated_data['title'], board=board, owner=user)
        if "description" in validated_data:
            task.description = validated_data['description']
        if "progress_status" in validated_data:
            task.progress_status = validated_data['progress_status']
        if "priority" in validated_data:
            task.priority = validated_data['priority']
        if "owner" in validated_data:
            task.owner = validated_data['owner']
        # Try to save the task, then return
        try:
            task.save()
        except Exception as e:
            raise e

        return task  # Finally return the task
