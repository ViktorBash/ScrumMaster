from rest_framework import serializers
from .models import Board, SharedUser, Task
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework import exceptions


# Board create serializer for POST requests
class BoardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        # Only the "title" field will be writable
        model = Board
        fields = ['title', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        # This piece gets the user object from the request.
        # If there is no user in the request a validation error is raised.
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
        except IntegrityError as e:  # Integrity error if the user already has a board with this name, since name is
            # unique for every owner in the Board model
            error_dict = {"title": ["You already have a board with this title."]}
            raise serializers.ValidationError(error_dict)
        return board  # Return board object


# GET request for the info on a board
class BoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']  # Read only, title is only thing that can be updated


# Shared User serializer
# CHECK: if board exists, if user exists, if owner,
class SharedUserCreateSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()
    shared_user_email = serializers.EmailField()

    def create(self, validated_data):
        # Check if board exists
        try:
            board = Board.objects.get(id=validated_data['id'])
        except Exception:
            raise exceptions.NotFound

        # Check if owner, and if owner of board
        owner = None
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            owner = request.user
        if owner is None or board.owner != owner:
            raise exceptions.NotFound

        # Check if shared_user
        try:
            user = User.objects.get(email=validated_data['shared_user_email'])
        except Exception:
            raise exceptions.NotFound

        # Put it together, create the shared user
        shared_user = SharedUser.objects.create(board=board, shared_user=user)
        shared_user.save()
        return shared_user



#
#
# # Task serializer
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"
