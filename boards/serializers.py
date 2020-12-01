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


# Board update serializer for PUT requests
class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']  # Read only, title is only thing that can be updated


# Board Info serializer. Takes in the ID of the board.
# For to_representation(), it will return all of the board info (board, owner, tasks, shared_users)
class BoardInfoSerializer(serializers.Serializer):
    board_id = serializers.IntegerField()  # Only input is the ID of the board

    # For API response, returns the board, owner, tasks and shared_users in a dictionary.
    def to_representation(self, instance):
        board = Board.objects.get(id=instance)

        owner_info = {
            "id": board.owner_id,
            "username": board.owner.username,
            "first_name": board.owner.first_name,
            "last_name": board.owner.last_name,
            "email": board.owner.email,
        }

        # Put the owner info inside the board info
        board_info = {
            "id": board.id,
            "title": board.title,
            "owner": owner_info,
            "url": board.url,
        }

        # Get tasks and put them into a list
        tasks = Task.objects.all().filter(board_id=instance)

        task_info = []

        if tasks:
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "date_created": task.date_created,
                    "title": task.title,
                    "description": task.description,
                    "progress_status": task.progress_status,
                    "priority": task.priority,
                    "owner": {
                        "id": task.owner_id,
                        "username": task.owner.username,
                        "first_name": task.owner.first_name,
                        "last_name": task.owner.last_name,
                        "email": task.owner.email,
                    }
                }
                task_info.append(task_dict)

        # Get shared users
        shared_users = SharedUser.objects.all().filter(board_id=instance)
        shared_user_info = []
        if shared_users:
            for shared_user in shared_users:
                shared_user_dict = {
                    "id": shared_user.id,
                    "username": shared_user.shared_user.username,
                    "first_name": shared_user.shared_user.first_name,
                    "last_name": shared_user.shared_user.last_name,
                    "email": shared_user.shared_user.email,
                }
                shared_user_info.append(shared_user_dict)

        # Compile all of the info and return it as a dictionary
        return_info = {
            "board": board_info,  # This is also where the owner info resides
            "tasks": task_info,
            "shared_users": shared_user_info,
        }
        return return_info

# Takes in the URL of a board instead of the ID, does same thing as BoardInfoSerializer
class BoardInfoUrlSerializer(serializers.Serializer):
    board_url = serializers.UUIDField()

    # For API response, returns the board, owner, tasks and shared_users in a dictionary.
    def to_representation(self, instance):
        board = Board.objects.get(url=instance)

        owner_info = {
            "id": board.owner_id,
            "username": board.owner.username,
            "first_name": board.owner.first_name,
            "last_name": board.owner.last_name,
            "email": board.owner.email,
        }



        # Get tasks and put them into a list
        tasks = Task.objects.all().filter(board_id=board.id)

        task_info = []

        if tasks:
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "date_created": task.date_created,
                    "title": task.title,
                    "description": task.description,
                    "progress_status": task.progress_status,
                    "priority": task.priority,
                    "owner": {
                        "id": task.owner_id,
                        "username": task.owner.username,
                        "first_name": task.owner.first_name,
                        "last_name": task.owner.last_name,
                        "email": task.owner.email,
                    }
                }
                task_info.append(task_dict)

        # Get shared users
        shared_users = SharedUser.objects.all().filter(board_id=board.id)
        shared_user_info = []
        if shared_users:
            for shared_user in shared_users:
                shared_user_dict = {
                    "id": shared_user.id,
                    "username": shared_user.shared_user.username,
                    "first_name": shared_user.shared_user.first_name,
                    "last_name": shared_user.shared_user.last_name,
                    "email": shared_user.shared_user.email,
                }
                shared_user_info.append(shared_user_dict)

        # Put the owner info inside the board info
        board_info = {
            "id": board.id,
            "title": board.title,
            "owner": owner_info,
            "url": board.url,
            "tasks": task_info,
            "shared_users": shared_user_info,
        }
        return board_info

        # Compile all of the info and return it as a dictionary
        # return_info = {
        #     "board": board_info,  # This is also where the owner info resides
        #     "tasks": task_info,
        #     "shared_users": shared_user_info,
        # }
        # return return_info


class BoardListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()  # Only parameter we take in is user id

    # Used for returning a JSON response with all of the boards
    def to_representation(self, instance):
        # Find boards owned by user, then put them into a list with proper info
        owned_boards = Board.objects.all().filter(owner_id=instance)
        owned_boards_list = []

        if owned_boards:
            # Since the owner info is the same, we will only query for it once at the beginning and then just use
            # the data multiple times in order to save database queries.
            owner_info_dict = {
                "id": owned_boards[0].owner.id,
                "username": owned_boards[0].owner.username,
                "first_name": owned_boards[0].owner.first_name,
                "last_name": owned_boards[0].owner.last_name,
                "email": owned_boards[0].owner.email,
            }

            for owned_board in owned_boards:
                owner_board_dict = {
                    "id": owned_board.id,
                    "title": owned_board.title,
                    "owner": owner_info_dict,
                    "url": owned_board.url,
                }
                # Add the info of the board to the owned_boards_list
                owned_boards_list.append(owner_board_dict)

        # Get the boards the user has been shared to, (aka for each shared user object get shared_user.board)
        shared_boards_list = []
        shared_users = SharedUser.objects.all().filter(shared_user_id=instance)
        if shared_users:
            shared_boards = [shared_user.board for shared_user in shared_users]
            # Go through and store every board in the list
            for shared_board in shared_boards:
                owner_info_dict = {
                    "id": shared_board.owner_id,
                    "username": shared_board.owner.username,
                    "first_name": shared_board.owner.first_name,
                    "last_name": shared_board.owner.last_name,
                    "email": shared_board.owner.email,
                }
                shared_board_dict = {
                    "id": shared_board.id,
                    "title": shared_board.title,
                    "owner": owner_info_dict,
                    "url": shared_board.url,
                }
                shared_boards_list.append(shared_board_dict)

        # Return the owned boards and shared boards as dict which will become JSON response
        return_info = {
            "owned_boards": owned_boards_list,
            "shared_boards": shared_boards_list,
        }
        return return_info


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

# Not needed at the moment
# # For GET requests
# class SharedUserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SharedUser
#         fields = ['board', 'shared_user']
#         read_only_fields = ['board', 'shared_user']


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
