from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views

# Connecting APIs to respective URLs
urlpatterns = [
    path('api/auth/register/', RegisterAPI.as_view()),
    path('api/auth/login/', LoginAPI.as_view()),
    path('api/auth/user/', UserAPI.as_view()),
    # knox includes: we wil only be using the logout view as we overwrote the other ones
    # api/auth/login --> Login view
    # api/auth/logout --> Logout view
    # api/auth/logoutall --> Logout all view
    path('api/auth/', include('knox.urls')),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name="knox_logout"),

]
