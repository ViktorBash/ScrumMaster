from django.contrib import admin
from .models import Board, SharedUser, Task
# Register your models here.

admin.site.register(Board)
admin.site.register(SharedUser)
admin.site.register(Task)
