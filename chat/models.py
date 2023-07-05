from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=70)
    dob = models.DateField()
    profile_image = models.ImageField(upload_to="media/profile_image")

    def __str__(self):
        return self.name
    
class ChatRooms(models.Model):
    user = models.ManyToManyField(User)
    chatroom = models.CharField(max_length=200)
    name = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.chatroom

class ChatMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.CharField(blank=False, null=False, max_length=120)
    message = models.CharField(blank=True, null=True, max_length=500)
    media = models.FileField(upload_to='static/media/', null=True, blank=True)
    media_type = models.CharField(max_length=200, null=True, blank=True)
    group_name = models.CharField(max_length=200, null=False, blank=False, default="Not provided")
    message_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
