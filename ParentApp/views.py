from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ParentApp.models import Games,Users
from ParentApp.serializers import GamesSerializer,UsersSerializer

from django.core.files.storage import default_storage
import pandas as pd
from joblib import load
import os
import jwt
import datetime


dirname = os.path.dirname(__file__)
dtpath = os.path.join(dirname, 'ML\Models\dt.joblib')
dt = load(dtpath)
lrpath = os.path.join(dirname, 'ML\Models\lr.joblib')
lr = load(lrpath)

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = Users.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.UserId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'UserId': user.UserId,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'Game': user.Game.GameId,
            'GameResponses': user.Game.UserResponses,
            'UserPhonenumber': user.UserPhonenumber,
            'PhotoFileName': str(user.PhotoFileName)
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Users.objects.filter(UserId=payload['id']).first()
        serializer = UsersSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

@csrf_exempt
def gamesApi(request,id=0):
    if request.method=='GET':
        games = Games.objects.all()
        games_serializer=GamesSerializer(games,many=True)
        return JsonResponse({'games': games_serializer.data},safe=False)
    elif request.method=='POST':
        game_data=JSONParser().parse(request)
        games_serializer=GamesSerializer(data=game_data)
        if games_serializer.is_valid():
            games_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        game_data=JSONParser().parse(request)
        game=Games.objects.get(GameId=game_data['GameId'])
        games_serializer=GamesSerializer(game,data=game_data)
        if games_serializer.is_valid():
            games_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        game=Games.objects.get(GameId=id)
        game.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def usersApi(request,id=0):
    if request.method=='GET':
        users = Users.objects.all()
        users_serializer=UsersSerializer(users,many=True)
        return JsonResponse(users_serializer.data,safe=False)
    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        users_serializer=UsersSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        user_data=JSONParser().parse(request)
        user=Users.objects.get(UserId=user_data['UserId'])
        users_serializer=UsersSerializer(user,data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        user=Users.objects.get(UserId=id)
        user.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)


@csrf_exempt
def predictApi(request, id=0):
    if request.method=='GET':
        game=Games.objects.get(GameId=id)
        my_answers=[[int(x) for x in game.UserResponses.split('.')]]
        columns=['bq1_num','bq2_num','bq3_num','q1_num','q2_num','q3_num']
        myrep=pd.DataFrame(my_answers,columns=columns)
        results_array=['Supportive','AGRESSIVE','Passive','HasExperiencedBullying +Supportive','HasExperiencedBullying + AGRESSIVE','HasExperiencedBullying + Passive','Empathetic','HasExperiencedBullying']
        game_data = {'Result': results_array[dt.predict(myrep)[0]-1]}
        games_serializer=GamesSerializer(game, data=game_data, partial=True)
        if games_serializer.is_valid():
            games_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Something went wrong!",safe=False)


