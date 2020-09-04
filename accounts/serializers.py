from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# User serializer (information about user)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "password",)
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False}
        }

    def create(self, validated_data):
        # Check if there is already user with this email
        try:  # Try to get an existing user and raise a validation error
            already_user = User.objects.get(email=validated_data['email'])
            error_dict = {"email": ['This email is already linked to an account']}
            raise serializers.ValidationError(error_dict)
        except serializers.ValidationError as e:  # pass up the validation error and raise it
            raise e
        except Exception as e:  # if there is no user this exception will cover it instead
            pass

        # Finally create object since everything is validated
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
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
