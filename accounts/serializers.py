from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# User serializer (information about user)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if "email" not in validated_data:
            raise serializers.ValidationError("email field required")
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


# Login serializer, is serializers.Serializer because we are not changing data in model
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)  # built in django func to see if user exists
        if user and user.is_active:  # if is a user and active, return user info
            return user
        # Else, raise validation error since it is not a valid user
        raise serializers.ValidationError("Incorrect Credentials")
