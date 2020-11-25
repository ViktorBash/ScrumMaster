from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import uuid

# TODO: make shared_user have attribute of can_create, can_edit, etc which is set by the owner of a board when they
#  join a board. Also, generally give the owner of a board more power. Also, is_viewer for people who are write only
#  also, needs_validation which forces owner to accept/reject tasks before putting it on the board


# one board is one project or scrum board
class Board(models.Model):
    title = models.CharField(max_length=100)  # title of the board
    owner = models.ForeignKey(User, related_name="board", on_delete=models.CASCADE)  # who owns/creates the board
    created_at = models.DateTimeField(auto_now_add=True)  # when it was created
    url = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = ['title', 'owner']

    def __str__(self):
        return self.title

    def __repr__(self):
        return {
            "object": "BOARD",
            "title": self.title,
            "id": self.id,
            "owner_username": self.owner.username,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "UUID": self.url,
        }


# many-to-one, users who are shared to a specific board
class SharedUser(models.Model):
    board = models.ForeignKey(Board, related_name="shared_users", on_delete=models.CASCADE)  # board allowed on
    # user allowed on the board
    shared_user = models.ForeignKey(User, related_name="shared_boards", on_delete=models.CASCADE)

    def __str__(self):
        return f"SHARED USER OBJECT. Board: \"{self.board}\", Shared user: \"{self.shared_user}\""

    def __repr__(self):
        return {
            "object": "SHARED USER",
            "id": self.id,
            "board": self.board,
            "board_id": self.board_id,
            "shared_user": self.shared_user,
            "shared_user_id": self.shared_user_id,
        }

    # this ensures there can be no duplicate shared user models (ie, you can't be shared to a board twice)
    def validate_unique(self, exclude=None, *args, **kwargs):
        super(SharedUser, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(board=self.board, shared_user=self.shared_user).exists():
            raise ValidationError(message="SharedUser with this board and name already exists")


# many-to-one, many tasks in one board
class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")  # board the task belongs to
    date_created = models.DateTimeField(auto_now_add=True)  # when created
    title = models.CharField(max_length=100, unique=True, default="Title")  # title, unique so no copies
    description = models.TextField(default="")  # description, can be left blank aka ""
    progress_status = models.CharField(max_length=50, default="WORKING")  # the progress of the task, ex:
    # STUCK [Red], WORKING [Blue], DONE [Green], ARCHIVED [Greyed out], FUTURE [another color]

    # who is in charge/owns the task, transferable/updatable, can be null
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # priority of thing, from 1 --> 5
    priority = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"TASK OBJECT. Board: \"{self.board.title}\", task: \"{self.title}\""

    def __repr__(self):
        return {
            "object": "TASK",
            "id": self.id,
            "board": self.board,
            "board_id": self.board_id,
            "title": self.title,
            "description": self.description,
            "progress_status": self.progress_status,
            "date_created": self.date_created,
            "owner": self.owner,
            "priority": self.priority
        }