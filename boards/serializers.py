from rest_framework import serializers
from .models import Board, SharedUser, Task
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


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
# class SharedUserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SharedUser
#         fields = "__all__"  # board and shared user (both foreign key objects)
#
#     def create(self, validated_data):
#         owner = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             owner = request.user
#         if owner is None:
#             raise serializers.ValidationError("Incorrect Credentials")
#         try:
#             board = Board.objects.get(id=validated_data['id'])
#         except Exception as e:
#             return "Board doesn't exist"
#         if board.owner != owner:
#             raise serializers.ValidationError("Incorrect Credentials")
#
#         # at this point, the board exists and the owner is the board owner
#         if 'email' in validated_data:
#             try:
#                 user = User.objects.get(email=validated_data['email'])
#             except Exception as e:
#                 return str(e)
#         elif 'username' in validated_data:
#             try:
#                 user = User.objects.get(username=validated_data['username'])
#             except Exception as e:
#                 return str(e)
#         else:
#             return "provide username or email"
#         try:
#             shared_user = SharedUser.objects.create(owner=owner, shared_user=user)
#             shared_user.save()
#             return shared_user
#         except Exception as e:
#             raise Exception
#
#

#
#
# # Task serializer
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"
