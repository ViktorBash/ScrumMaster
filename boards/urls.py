from django.urls import path
from .api import BoardCreate, BoardInfo, BoardList

urlpatterns = [
    path('api/board/create/', BoardCreate.as_view()),
    path('api/board/info/<int:pk>/', BoardInfo.as_view()),
    path('api/board/list/', BoardList.as_view()),
]
