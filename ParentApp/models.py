from operator import mod
from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Games(models.Model):
    GameId = models.AutoField(primary_key=True)
    GameLevel = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CharacterColor = models.CharField(max_length=500)
    CharacterName = models.CharField(max_length=500)
    CharacterGender = models.CharField(max_length=500)
    UserResponses = models.CharField(max_length=500, null=True, blank=True)
    Result = models.CharField(max_length=500, null=True, blank=True)
    TimeSpentPlaying = models.IntegerField(default=0)
    NotifyParents = models.IntegerField(default=0)

class Users(AbstractUser):
    UserId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="null")
    email = models.CharField(max_length=255, unique=False, default="null")
    password = models.CharField(max_length=255,default="null")
    username = models.CharField(max_length=255,unique=True,default=email)
    childName = models.CharField(max_length=255,default="null")
    childAge = models.CharField(max_length=255,default="null")
    isChildDepressed = models.CharField(max_length=255,default="null")
    isChildBullied = models.CharField(max_length=255,default="null")
    describeYourChildBehaviour = models.CharField(max_length=255,default="null")
    Game = models.ForeignKey(Games, on_delete=models.CASCADE, default=Games.objects.latest('GameId').GameId)
    UserPhonenumber = models.CharField(max_length=500)
    PhotoFileName = models.ImageField(upload_to='Photos')
    #USERNAME_FIELD = []
    REQUIRED_FIELDS = []
