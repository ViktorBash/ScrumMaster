from django.urls import path
from .api import BoardCreate, BoardInfo, BoardList, SharedUserCreate

urlpatterns = [
    path('api/board/create/', BoardCreate.as_view()),
    path('api/board/<int:pk>/', BoardInfo.as_view()),  # For retrieve, update and delete (Aka GET, PUT, DELETE)
    path('api/board/list/', BoardList.as_view()),  # get list of shared boards and owned boards
    path('api/shareduser/create/', SharedUserCreate.as_view()),
]
