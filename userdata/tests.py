import json
from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

class SocialnetworkTest(APITestCase):
    user = None
    profile = None
    chatroom = None
    picture = None
    userjson = {'id': 1, 'username': 'clarkkent', 'email': 'clark@kent.com'}
    profilejson = {'id': 1, 'user': 1,'image':'/media/default.jpg'}
    chatroomjson = {'id': 1, 'name': 'Dining Room', 'profile': 1 }
    picturejson = {'id': 1, 'image':'images/clarkkent/nietzsche.PNG', 'profile': 1}

    def setUp(self):
        #this will automatically create a profile record due to the signal
        self.user = UserFactory.create()
        #self.chatroom = ChatroomFactory.create()

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Chatroom.objects.all().delete()
        Picture.objects.all().delete()
        Status.objects.all().delete()

    def test_userDetailReturnSuccess(self):        
        # use the api to return the user record created
        url = reverse('user_api', kwargs={'username': "clarkkent"})
        response = self.client.get(url)
        response.render()

        # check the response is good and the response by the api is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.userjson)

    # profle is automatically created whe user record id created
    # check that this is the case
    def test_profileDetailReturnSuccess(self):
        # use the api to return the profile record created
        url = reverse('profile_api', kwargs={'username': "clarkkent"})
        response = self.client.get(url)
        response.render()

        # check response is good, the profile user is mapped to the created user
        # and the image iss et to default
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user'], self.userjson['id'])
        self.assertEqual(response.json()['image'], self.profilejson['image'])

    # check that an an unknow user generates an error
    def test_unknownUser404Response(self):
        # use the api to return the response
        url = reverse('user_api', kwargs={'username': "humptydumpty"})
        response = self.client.get(url)

        # check the response is good and the response by the api is as expected
        self.assertEqual(response.status_code, 404)

    # test the chatroom is created with the right field values
    def test_chatroomDetailReturnSuccess(self):
        # use the api to return the picture detail
        url = reverse('chatroom_api', kwargs={'name': "Dining Room"})
        response = self.client.get(url)
        response.render()

        # check the response is good and the response by the api is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.chatroomjson)

    # test that a picture record can be created
    def test_pictureDetailReturnSuccess(self):
        # use the api to return the picture detail
        url = reverse('user_pictures_api', kwargs={'username': "clarkkent"})
        response = self.client.get(url)
        response.render()

        # check the response is good and the response by the api is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.picturejson)

