from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Picture, Chatroom, Status


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image', 'profile']


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['message', 'profile']
