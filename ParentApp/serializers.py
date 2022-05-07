from rest_framework import serializers
from ParentApp.models import Games,Users
from django.contrib.auth.hashers import make_password

class GamesSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Games
        fields=('GameId','GameLevel','created_at','updated_at','CharacterColor','CharacterName','CharacterGender','UserResponses','Result','TimeSpentPlaying','NotifyParents')

class UsersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta: 
        model = Users
        fields=('UserId','name','email','password','username','childName', 'childAge', 'isChildDepressed', 'isChildBullied', 'describeYourChildBehaviour', 'UserPhonenumber','PhotoFileName')
        extra_kwargs = {
            'password': {'write_only': True}
        }

