from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from knox.auth import TokenAuthentication


# Register API, post request
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # If bad data, exception would raise and rest of code would not run
        user = serializer.save()  # Saving to serializer which then saves to database
        # Sending a response giving the info of the user and a token for them to use as well
        return Response({
            # using user serializer to get the ID, username and email for our response
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],  # Create token for user to use
        })


# Login API, post request
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    authentication_classes = (TokenAuthentication,)  #

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # calling login serializer
        serializer.is_valid(raise_exception=True)  # Raise exception if username and password not valid/true
        user = serializer.validated_data
        # Same response as register, give
        return Response({
            # using user serializer to get the ID, username and email for our response
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],  # Create token for user to use
        })


# User API (get) info about user
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
