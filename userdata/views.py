from django.contrib.auth import login
from django.forms.utils import from_current_timezone
from .models import Picture, User, Profile, Chatroom, Status
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import *
import datetime
from django.db.models import Q

def index(request):
    date = datetime.date.today()
    context = {'author': 'Wesley Persad', 'date': date}
    return render(request, 'userdata/index.html', context)

def register(request):
    # check if the form has been submitter with data via POST
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account Created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    date = datetime.date.today()
    context = {'author': 'Wesley Persad', 'date': date}
    context['form'] = form
    return render(request, 'userdata/register.html', context)

@login_required
def profile(request, *args, **kwargs):
    date = datetime.date.today()

    # check if a pk of a profile has been sent
    if not kwargs == {}:
        pk = kwargs['pk']
        # get the profile of the pk passed in
        profile = Profile.objects.get(pk=pk)
        user = profile.user
    else:
        # get the user and profile of this logged in user
        user = request.user
        profile = request.user.profile

    # get our users friends and set user to be a friend
    # page callers list of friends and logged in users profile id
    friends = list(user.profile.friends.values_list(flat=True))
    loginuserid = request.user.profile.id

    # if I am a friend in this profile or i am looking at my own profile
    if (loginuserid in friends) or (loginuserid == user.profile.id):
        friend = True
    else:
        friend = False

    # get all the pictures that are linked via fk to this profile
    pictures = Picture.objects.filter(profile=profile)

    # get all the chatrooms that are linked via fk to this profile
    chatrooms = Chatroom.objects.filter(profile=profile)

    # get all the messages for this this user
    statuses = Status.objects.filter(profile=profile)

    # check if the form has been submitter with data via POST
    if request.method == 'POST':
        s_form = StatusUpdateForm(request.POST, instance=profile)
        if s_form.is_valid():
            # s_form.dave does not seem to work so will create a status object
            # directly from form POST data
            f_message = s_form.cleaned_data['message']
            f_profile = s_form.cleaned_data['profile']

            Status.objects.create(message=f_message, profile=f_profile)
            # s_form.save()

            messages.success(request, f'Your status message has been added !')
            return redirect('profile')
    else:
        s_form = StatusUpdateForm(initial={'profile': profile})

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'user': user,
        'profile': profile,
        'friend': friend,
        's_form': s_form,
        'pictures': pictures,
        'chatrooms': chatrooms,
        'statuses': statuses
    }
    return render(request, 'userdata/profile.html', context)

@login_required
def profiles(request):
    date = datetime.date.today()
    chatrooms = Chatroom.objects.all()

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    # exclude logged in user
    profiles = Profile.objects.exclude(id=loginuser)

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus,
        'chatrooms': chatrooms
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def editprofile(request):
    date = datetime.date.today()

    # get the user and profile of this logged in user
    user = request.user
    profile = request.user.profile

    # check if the form has been submitter with data via POST
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'user': user,
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userdata/editprofile.html', context)

@login_required
def friends(request):
    date = datetime.date.today()
    chatrooms = Chatroom.objects.all()

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    # get id of friend profiles
    friendlist = list(request.user.profile.friends.values_list(flat=True))

    profiles = Profile.objects.filter(id__in=friendlist)

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus,
        'chatrooms': chatrooms
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def friend(request, pk):
    # make profile with id=pk a friend
    date = datetime.date.today()
    profiles = Profile.objects.all()

    # first add profile with id = pk from the logged in users friends list
    request.user.profile.friends.add(pk)

    # also need to remove request from from profile with id=pk
    request.user.profile.requests.remove(pk)

    # send a message about request
    profile = Profile.objects.get(id=pk)
    messages.success(request, f"You Have Become A Friend Of {profile.user}")

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users, isFriends and beFriends lists so we can iterate in the template
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def unfriend(request, pk):
    # unfriend profile with id=pk
    date = datetime.date.today()
    profiles = Profile.objects.all()

    # first remove profile with id = pk from the logged in users friends list
    request.user.profile.friends.remove(pk)

    # send a message about request
    profile = Profile.objects.get(id=pk)
    messages.success(request, f"You Are No Loger A Friend Of {profile.user}")

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def friendreq(request, pk):
    # request that profile with id=pk has the logged on user's id
    date = datetime.date.today()
    profiles = Profile.objects.all()

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    # first get the profile of the id=pk and add the id of the logged in
    # user to it's friend request field
    profile = Profile.objects.get(id=pk)
    profile.requests.add(loginuser)

    # send a message about request
    messages.success(
        request, f"You Have Sent A Friend Request to {profile.user}")

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def friendrej(request, pk):
    # reject that request from profile with id=pk from logged on users requests
    date = datetime.date.today()
    profiles = Profile.objects.all()

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    # first remove the profile of the id=pk from the logged in user request field
    profile = Profile.objects.get(id=pk)
    request.user.profile.requests.remove(pk)

    # send a message about request
    messages.success(
        request, f"You Have Rejected A Friend Request from {profile.user}")

    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def addpicture(request):
    date = datetime.date.today()

    if request.method == "GET":
        profile = request.user.profile
        form = PictureUpdateForm(initial={'profile': profile})
        context = {
            'author': 'Wesley Persad',
            'date': date,
            "form": form
        }
        return render(request, 'userdata/addpicture.html', context)
    elif request.method == "POST":
        form = PictureUpdateForm(request.POST or None, request.FILES or None, 
                                    instance=request.user.profile)

        if form.is_valid():
            # form.save() does not seem to work so will create a status
            # object directly from the form POST data
            Picture.objects.create(image=form.cleaned_data['image'], 
                                    profile=form.cleaned_data['profile'])

            #form.save()
            messages.success(request, f'New Picture Added !')
            #redirect to the updated personal profile
            return redirect('profile')
        else:
            messages.error(request, f'Problem With Input !')
            return HttpResponseRedirect('/')

@login_required
def room(request, room_name):
    date = datetime.date.today()
    loginuser = request.user.profile.user.username

    # create a new room if it does not already exist
    try:
        # see if it exists already
        chatroom = Chatroom.objects.get(name=room_name)
    except:
        # create a new chatroon it if it does not
        Chatroom.objects.create(name=room_name, profile=request.user.profile)

    # get the owner
    chatroom = Chatroom.objects.get(name=room_name)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'room_name': room_name,
        'owner': chatroom.profile.user,
        'loginuser': loginuser
    }
    return render(request, 'userdata/room.html', context)

@login_required
def search_profiles(request):
    date = datetime.date.today()
    chatrooms = Chatroom.objects.all()

    # for all users determine if they are the friend of the logged in user
    isFriends = []
    loginuser = request.user.profile.id

    # process list for a POST request
    if request.method == "POST" and request.POST["searched"] != '':
        searched = request.POST["searched"]
        # use a Q object to search in username or email field
        profiles = Profile.objects.filter(Q(user__username__icontains=searched) |
                                            Q(user__email__icontains=searched))
    else:
        # exclude logged in user
        profiles = Profile.objects.all()

    # process the data for the profiles
    for profile in profiles:
        friends = list(profile.friends.values_list(flat=True))
        if loginuser in friends:
            isFriends.append(True)
        else:
            isFriends.append(False)

    # find out if a user has made a friend requested to the logged in user
    beFriends = []
    requests = list(request.user.profile.requests.values_list(flat=True))

    for profile in profiles:
        if profile.id in requests:
            beFriends.append(True)
        else:
            beFriends.append(False)

    # join the users and the isFriend lists so we can iterate
    profilesplus = zip(profiles, isFriends, beFriends)

    context = {
        'author': 'Wesley Persad',
        'date': date,
        'profilesplus': profilesplus,
        'chatrooms': chatrooms
    }
    return render(request, 'userdata/profiles.html', context)

@login_required
def status(request):
    date = datetime.date.today()

    if request.method == "GET":
        profile = request.user.profile
        form = StatusUpdateForm(initial={'profile': profile})
        context = {
            'author': 'Wesley Persad',
            'date': date,
            "form": form
        }
        return render(request, 'userdata/status.html', context)
    elif request.method == "POST":
        form = StatusUpdateForm(request.POST,
                                instance=request.user.profile)

        if form.is_valid():
            # s_form.dave does not seem to work so will create a status object
            # directly from form POST data
            f_message = form.cleaned_data['message']
            f_profile = form.cleaned_data['profile']

            Status.objects.create(message=f_message, profile=f_profile)
            form.save()

            messages.success(request, f'New Message Added !')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, f'Problem With Input !')
            return HttpResponseRedirect('/')
