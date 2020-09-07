from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status

"""
tests.py doesn't just test regular conditions, it also tests validation to make sure that errors are being given
correctly when a bad request is made, (ex: giving wrong password when logging in)

Testing Currently Covered:
Registration
    -Correct Registration
    -Registering user with missing information
    -Registering user with existing username
    -Registering user with existing email
    -Registering with weak password
Login
    -Correct credentials
    -Wrong credentials
    -Missing credentials
User API view
    -With correct token
    -With incorrect token
    -With no token
Logging out
    -with correct token
    -with wrong token
    -with no token
    
TODO: Test wrong requests (ex: POST, PUT, DELETE, etc) 
"""


# Register an account that has no errors, should be success
class AccountRegisterSuccess(TestCase):
    def setUp(self):
        # The variables used for account setup
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"

    def test_register(self):
        url = "/api/auth/register/"
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")

        # Status code test
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Model instance is correct in database tests
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, self.first_name)
        self.assertEqual(User.objects.get().last_name, self.last_name)
        self.assertEqual(User.objects.get().username, self.username)
        self.assertEqual(User.objects.get().email, self.email)
        self.assertTrue(User.objects.get().password)

        # Response gives correct information test
        self.assertEqual(response.data['user']['username'], self.username)
        self.assertEqual(response.data['user']['first_name'], self.first_name)
        self.assertEqual(response.data['user']['last_name'], self.last_name)
        self.assertEqual(response.data['user']['email'], self.email)

    def tearDown(self):
        User.objects.all().delete()


# Register account with no information given, should receive several errors
class AccountRegisterFail1(TestCase):
    def setUp(self):
        # The variables used for account setup
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"

    def test_register(self):
        url = "/api/auth/register/"
        data = {}
        response = self.client.post(url, data, format="json")

        # Status code test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Model instance is correct in database tests
        self.assertEqual(User.objects.count(), 0)

        # Response gives correct information test
        self.assertEqual(response.data['first_name'], ["This field is required."])
        self.assertEqual(response.data['last_name'], ["This field is required."])
        self.assertEqual(response.data['username'], ["This field is required."])
        self.assertEqual(response.data['email'], ["This field is required."])
        self.assertEqual(response.data['password'], ["This field is required."])

    def tearDown(self):
        User.objects.all().delete()


# Register user with an existing email, should give error
class AccountRegisterFail2(TestCase):
    def setUp(self):
        # Creating the original user via post request
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"

        # Setting these variables to class variables since we will just reuse them in the actual function
        self.url = "/api/auth/register/"
        self.data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(self.url, self.data, format="json")

    def test_register(self):
        self.data['username'] = 'Bob2'
        response = self.client.post(self.url, self.data, format="json")

        # Status code test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Error code tests
        self.assertEqual(response.data['email'], ['A user with that email already exists.'])

    def tearDown(self):
        User.objects.all().delete()


# Register user with an existing username, should give error. (Note: email is also the same but only username error
# is returned because this is the behavior of the API).
class AccountRegisterFail3(TestCase):
    def setUp(self):
        # Creating the original user via post request
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"

        # Setting these variables to class variables since we will just reuse them in the actual function
        self.url = "/api/auth/register/"
        self.data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(self.url, self.data, format="json")

    def test_register(self):
        response = self.client.post(self.url, self.data, format="json")

        # Status code test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Error code tests
        self.assertEqual(response.data['username'], ['A user with that username already exists.'])

    def tearDown(self):
        User.objects.all().delete()


# Login to an account with no errors
class AccountLoginSuccess(TestCase):
    def setUp(self):
        # Creating a user via post request
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"
        url = "/api/auth/register/"
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")

    def test_login(self):
        url = "/api/auth/login/"
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(url, data, format="json")

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response gives correct information
        self.assertEqual(response.data['user']['username'], self.username)
        self.assertEqual(response.data['user']['first_name'], self.first_name)
        self.assertEqual(response.data['user']['last_name'], self.last_name)
        self.assertEqual(response.data['user']['email'], self.email)

        self.assertTrue(response.data['token'])

    def tearDown(self):
        User.objects.all().delete()


# Try to login with wrong password, should give error
class AccountLoginFail1(TestCase):
    def setUp(self):
        # Creating a user via post request
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"

        url = "/api/auth/register/"
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")

    def test_login(self):
        url = "/api/auth/login/"
        WRONG_PASSWORD = "wrong"

        data = {
            "username": self.username,
            "password": WRONG_PASSWORD,
        }
        response = self.client.post(url, data, format="json")

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test Errors
        self.assertEqual(response.data['non_field_errors'], ['Incorrect Credentials'])

    def tearDown(self):
        pass


# Try to login with missing credentials, should give errors
class AccountLoginFail2(TestCase):
    def setUp(self):
        pass

    def test_login(self):
        url = "/api/auth/login/"
        data = {}
        response = self.client.post(url, data, format="json")

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test Errors
        self.assertEqual(response.data['password'], ['This field is required.'])
        self.assertEqual(response.data['username'], ['This field is required.'])

    def tearDown(self):
        User.objects.all().delete()


# Test that can logout account with token successfully, should give no errors
class AccountLogoutSuccess(TestCase):
    def setUp(self):

        # Create a user
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"
        url = "/api/auth/register/"
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")

        # Login the user
        url = "/api/auth/login/"
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(url, data, format="json")

        # Get the token
        self.token = response.data['token']

    def test_logout(self):
        url = "/api/auth/logout/"
        data = {}
        # Set the token as the authorization header
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Token {self.token}"
        response = self.client.post(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        User.objects.all().delete()


# Try to logout user with the wrong token
class AccountLogoutFail1(TestCase):
    def setUp(self):
        pass

    def test_logout(self):
        url = "/api/auth/logout/"
        data = {}
        # Set the token as the authorization header
        self.WRONG_TOKEN = "WRONGTOKEN"
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Token {self.WRONG_TOKEN}"
        response = self.client.post(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test error
        self.assertEqual(response.data['detail'], "Invalid token.")

    def tearDown(self):
        User.objects.all().delete()


# Try to logout with no credentials, should give error
class AccountLogOutFail2(TestCase):
    def setUp(self):
        pass

    def test_logout(self):
        url = "/api/auth/logout/"
        response = self.client.post(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test error code
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def tearDown(self):
        User.objects.all().delete()


# Try to get user information, should be success
class AccountUserSuccess(TestCase):
    def setUp(self):
        # Create a user
        self.first_name = "Bob"
        self.last_name = "Smith"
        self.username = "Bob475"
        self.email = "bob@gmail.com"
        self.password = "Ilovehotdogs17"
        url = "/api/auth/register/"
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")

        # Login the user
        url = "/api/auth/login/"
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(url, data, format="json")

        # Get the token
        self.token = response.data['token']

    def test_user(self):
        url = "/api/auth/user/"
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Token {self.token}"
        response = self.client.get(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test response gives correct information
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['first_name'], self.first_name)
        self.assertEqual(response.data['last_name'], self.last_name)
        self.assertEqual(response.data['email'], self.email)


    def tearDown(self):
        User.objects.all().delete()


# Try to get user information with the wrong token, should give error
class AccountUserFail1(TestCase):
    def setUp(self):
        pass

    def test_user(self):
        self.WRONG_TOKEN = "WRONGTOKEN"
        url = "/api/auth/user/"
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Token {self.WRONG_TOKEN}"
        response = self.client.get(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test error code
        self.assertEqual(response.data['detail'], "Invalid token.")

    def tearDown(self):
        User.objects.all().delete()


# Try to get user information with no token, should give error
class AccountUserFail2(TestCase):
    def setUp(self):
        pass

    def test_user(self):
        url = "/api/auth/user/"
        response = self.client.get(url)

        # Test correct status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test error code
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def tearDown(self):
        User.objects.all().delete()
