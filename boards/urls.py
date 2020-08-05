from django.urls import path
from .api import BoardCreate

urlpatterns = [
    path('api/board/create/', BoardCreate.as_view())
]
