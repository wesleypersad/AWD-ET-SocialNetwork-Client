from django.contrib import admin
from .models import Profile, Picture, Chatroom, Status

admin.site.register(Profile)

admin.site.register(Picture)

admin.site.register(Chatroom)

admin.site.register(Status)
