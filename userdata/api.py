from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['GET'])
def user_detail(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserListSerializer(user)
        return Response(serializer.data)

@api_view(['GET'])
def user_list(request):
    try:
        user = User.objects.all()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def profile_detail(request, username):
    if not request.user.is_authenticated:
        return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileListSerializer(profile)
        return Response(serializer.data)

@api_view(['GET'])
def profile_list(request):
    try:
        profile = Profile.objects.all()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileListSerializer(profile, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def chatroom_detail(request, name):
    try:
        chatroom = Chatroom.objects.get(name=name)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChatroomListSerializer(chatroom)
        return Response(serializer.data)

@api_view(['GET'])
def chatroom_list(request):
    try:
        chatroom = Chatroom.objects.all()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChatroomListSerializer(chatroom, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def user_picture_list(request, username):
    try:
        picture = Picture.objects.filter(profile__user__username=username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PictureListSerializer(picture, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def picture_list(request):
    try:
        picture = Picture.objects.all()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PictureListSerializer(picture, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def user_message_list(request, username):
    try:
        message = Status.objects.filter(profile__user__username=username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageListSerializer(message, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def content_message_list(request, content):
    try:
        message = Status.objects.filter(message__contains=content)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageListSerializer(message, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def message_list(request):
    try:
        message = Status.objects.all()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageListSerializer(message, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def userpage(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user__username=username)
        picture = Picture.objects.filter(profile__user__username=username)
        message = Status.objects.filter(profile__user__username=username)
        chatroom = Chatroom.objects.filter(profile__user__username=username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # This is essentially the combination of the 'username' subroutines above
    if request.method == 'GET':
        serializer1 = UserListSerializer(user)
        serializer2 = ProfileListSerializer(profile)
        serializer3 = PictureListSerializer(picture, many=True)
        serializer4 = MessageListSerializer(message, many=True)
        serializer5 = ChatroomListSerializer(chatroom, many=True)

        return Response({
                        "user":serializer1.data, 
                        "profile":serializer2.data,
                        "pictures":serializer3.data,
                        "messages":serializer4.data,
                        "chatrooms":serializer5.data 
                        })

# let's add a status message using POST
@api_view(['POST'])
def addmessage(request):
    # check that if does not exist
    try:
        message = request.data["message"]
        profile = request.data["profile"]
    except KeyError:
        return HttpResponseRedirect('/')

    # update the message fieled with the id
    request.data.update({
                            "message": message,
                            "profile": profile
                        })

    serializer = MessageListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

# let's add a chatroom using POST
@api_view(['POST'])
def addchatroom(request):
    # check that if does not exist
    try:
        name = request.data["name"]
        profile = request.data["profile"]
    except KeyError:
        return HttpResponseRedirect('/')

    # update the message fieled with the id
    request.data.update({
                            "name": name,
                            "profile": profile
                        })

    serializer = ChatroomListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)