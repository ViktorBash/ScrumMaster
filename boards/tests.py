from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.
"""
Note:
Create tests that are 3-4 of the bullet points. That way there is one large setup and then multiple functions
representing each bullet point for the tests. This will reduce the need for setting up and tearing down excessively.


Things that must be tested:

BoardCreate:
    -try and create board
    -try and create board without info
    -try and create board with same title
BoardInfo:
    -try and get board as owner
    -try and get board as shared user
    -try and get board without being owner or shared user

    -try and delete board as owner
    -try and delete board as shared user
    -try and delete board as not owner or shared user
    
    -try and put board as owner
    -try and put board as shared user
    -try and put board as not owner or shared user
    
BoardList:
    -try and list boards (shared to and owned)
    
SharedUserCreate:
    -try and create shared user as owner
    -try and create shared user with missing info
    -try and create shared user as shared user
    -try and create shared user without being owner or shared user

SharedUserDelete:
    -try and delete shared user as owner
    -try and delete shared user with missing info
    -try and delete shared user as shared user
    -try and delete shared user without being owner or shared user
    
TaskCreate:
    -Try and create task as owner
    -Try and create task as shared user
    -Try and create task without being owner or shared user
    -Try and create task with missing information

TaskInfo:
    -Try and get task as owner
    -Try and get task as shared user
    -Try and get task without being owner or shared user
    -Try and get task with missing information
    
    -Try and put task as owner
    -Try and put task as shared user
    -Try and put task without being owner or shared user
    -Try and put task with missing information
    
    -Try and delete task as owner
    -Try and delete task as shared user
    -Try and delete task without being owner or shared user
    -Try and delete task with missing information
"""