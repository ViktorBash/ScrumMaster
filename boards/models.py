from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# TODO: make shared_user have attribute of can_create, can_edit, etc which is set by the owner of a board when they
#  join a board. Also, generally give the owner of a board more power. Also, is_viewer for people who are write only
#  also, needs_validation which forces owner to accept/reject tasks before putting it on the board


# one board is one project or scrum board
class Board(models.Model):
    title = models.CharField(max_length=100)  # title of the board
    owner = models.ForeignKey(User, related_name="board", on_delete=models.CASCADE)  # who owns/creates the board
    created_at = models.DateTimeField(auto_now_add=True)  # when it was created

    def __str__(self):
        return self.title


# many-to-one, users who are shared to a specific board
class SharedUser(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # board allowed on
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE)  # user allowed on the board

    def __str__(self):
        return f"SHARED USER OBJECT, board: {self.board}, shared user: {self.shared_user}"


# many-to-one, many tasks in one board
class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # board the task belongs to
    date_created = models.DateTimeField(auto_now_add=True)  # when created
    title = models.CharField(max_length=100, unique=True)  # title, unique so no copies
    description = models.TextField(default="")  # description, can be left blank aka ""
    progress_status = models.CharField(max_length=50)  # the progress of the task, ex:
    # STUCK [Red], WORKING [Blue], DONE [Green], ARCHIVED [Greyed out], FUTURE [another color]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # who is in charge/owns the task, transferable/updatable
    # priority of thing, from 1 --> 5
    priority = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"TASK, board: {self.board.title}, task: {self.title}"
