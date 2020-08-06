from rest_framework import serializers
from .models import Board, SharedUser, Task
from django.db.utils import IntegrityError

# Board create serializer for POST requests
class BoardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        # Only the "title" field will be writable
        model = Board
        fields = ['title', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        # This piece gets the user object from the request.
        # If there is no user in the request a validation error ir raised.
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
        except IntegrityError as e:
            return "You already have a board with that name"
        return board  # Return board object


# GET request for the info on a board
class BoardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'created_at']
        read_only_fields = ['id', 'title', 'owner', 'created_at']  # Read only to enforce it is used for GET requests

# # Shared User serializer
# class SharedUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SharedUser
#         fields = "__all__"
#
#
# # Task serializer
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"
