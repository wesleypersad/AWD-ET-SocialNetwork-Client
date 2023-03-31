from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views as userdata_views
from . import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # display the site homepage
    path('', userdata_views.index, name='index'),
    # register a new user
    path('register/', userdata_views.register, name='register'),
    # display the profile of the logged in user
    path('profile/', userdata_views.profile, name='profile'),
    # display the profile with a given pk
    path('profile/<int:pk>', userdata_views.profile, name='profile'),
    # get all the other profiles except the logged in user
    path('profiles/', userdata_views.profiles, name='profiles'),
    # edit the profile of the logged in user
    path('editprofile/', userdata_views.editprofile, name='editprofile'),
    # add a picture to the galler of the logged in user
    path('addpicture/', userdata_views.addpicture, name='addpicture'),
    # make a friend of a profile with id=pk
    path('friend/<int:pk>', userdata_views.friend, name='friend'),
    # find all the friends of the logged in user
    path('friends/', userdata_views.friends, name='friends'),
    # search for a particular user
    path('search/', userdata_views.search_profiles, name='search_profiles'),
    # enter an updated status message
    path('status/', userdata_views.status, name='status'),
    # unfriend profile with id=pk
    path('unfriend/<int:pk>', userdata_views.unfriend, name='unfriend'),
    # request to be the friend of profile with id=pk
    path('friendreq/<int:pk>', userdata_views.friendreq, name='friendreq'), 
    # reject the friend request from profile with id=pk
    path('friendrej/<int:pk>', userdata_views.friendrej, name='friendrej'), 
    path('room/<str:room_name>/', userdata_views.room, name='room'),
    path('login/', auth_views.LoginView.as_view(template_name='userdata/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userdata/logout.html'), name='logout'),

    # THE FOLLOWING ARE API PATHS FOR THE ENDTERM SPEC !!!
    # users
    path('api/user/<str:username>', api.user_detail, name='user_api'),
    path('api/users/', api.user_list, name='users_api'),
    # profiles
    path('api/profile/<str:username>', api.profile_detail, name='profile_api'),
    path('api/profiles/', api.profile_list, name='profiles_api'),
    # chatrooms
    path('api/chatroom/<str:name>', api.chatroom_detail, name='chatroom_api'),
    path('api/chatrooms/', api.chatroom_list),
    # pictures
    path('api/picture/<str:username>', api.user_picture_list, name='user_pictures_api'),
    path('api/pictures/', api.picture_list),
    # status messages
    path('api/messageuser/<str:username>', api.user_message_list),
    path('api/messagecontent/<str:content>', api.content_message_list),
    path('api/messages/', api.message_list),
    # get all data to build a profile page for a particular user
    path('api/userpage/<str:username>', api.userpage),
    # use a POST request to add a status message
    path('api/addmessage/', api.addmessage),
    # use a POST request to add a chatroom
    path('api/addchatroom/', api.addchatroom),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
