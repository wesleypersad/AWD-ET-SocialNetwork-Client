import factory

from random import randint
from random import choice
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    id = 1
    username = 'clarkkent'
    email = 'clark@kent.com'

    class Meta:
        model = User

class ProfileFactory(factory.django.DjangoModelFactory):
    id = 1
    user = factory.SubFactory(UserFactory)
    image = "/media/default.jpg"

    class Meta:
        model = Profile
        django_get_or_create = ('user',)

class PictureFactory(factory.django.DjangoModelFactory):
    id = 1
    image = "images/clarkkent/nietzsche.PNG"
    profile = factory.SubFactory(ProfileFactory)

    class Meta:
        model = Picture
        django_get_or_create = ('profile',)

class ChatroomFactory(factory.django.DjangoModelFactory):
    id = 1
    name = "Dining Room"
    profile = factory.SubFactory(ProfileFactory)

    class Meta:
        model = Chatroom
        django_get_or_create = ('profile',)

class StatusFactory(factory.django.DjangoModelFactory):
    id = 1
    message = "This is a test status message"
    profile = factory.SubFactory(ProfileFactory)

    class Meta:
        model = Status
        django_get_or_create = ('profile',)
