from django.urls import path
from .api import BoardCreate, BoardInfo

urlpatterns = [
    path('api/board/create/', BoardCreate.as_view()),
    path('api/board/info/<int:pk>/', BoardInfo.as_view()),
]
