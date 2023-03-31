from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # these are you current friends
    friends = models.ManyToManyField("self", blank=True)

    # these are your friend requests
    requests = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        # if the image is too big resize it
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    # method to add another profile(account) as friend
    def add_friend(self, profile):
        if not profile in self.friends.all():
            self.friends.add(profile)

    # method to remove an existing friend
    def remove_friend(self, profile):
        if profile in self.friends.all():
            self.friends.remove(profile)

    # account a friend of ours ?
    def is_friend(self, profile):
        if profile in self.friends.all():
            return True
        return False

    # add a friend request to another profile
    def add_request(self, profile):
        if not self in profile.requests.all():
            profile.requests.add(self)

    # cancel a friend request to another profile
    def remove_request(self, profile):
        if self in profile.friends.all():
            profile.requests.remove(self)

# create a class of picture to contain the gallery images for a profile
# we can then link a given image to a profile (user) using a profile field (foreign key)
def upload_gallery_image(instance, filename):
    return f"images/{instance.profile.user}/{filename}"

class Picture(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="picture")

# create a class to record the chatrooms created by a user(profile)
class Chatroom(models.Model):
    name = models.CharField(max_length=50, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# create a class of status messages for the user profiles
class Status(models.Model):
    message = models.CharField(max_length=200, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now, blank=True)
