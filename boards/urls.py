from django.urls import path
from .api import BoardCreate, BoardInfo, BoardList, SharedUserCreate, SharedUserDelete, TaskCreate, TaskInfo

urlpatterns = [
    path('api/board/create/', BoardCreate.as_view()),
    path('api/board/list/', BoardList.as_view()),  # get list of shared boards and owned boards
    path('api/board/<str:url>/', BoardInfo.as_view()),  # For retrieve, update and delete (Aka GET, PUT, DELETE)
    path('api/shareduser/create/', SharedUserCreate.as_view()),
    path('api/shareduser/delete/', SharedUserDelete.as_view()),
    path('api/task/create/', TaskCreate.as_view()),
    # path('api/task/<int:pk>/', TaskInfo.as_view()),
]
