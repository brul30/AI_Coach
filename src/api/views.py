from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
#from .serializers import ProductSerializer


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from api.utility import make_openAI_request

import requests
import json
import os
from openai import OpenAI
# @api_view(['GET'])
# def get_Data(request):
#     #person = {'name':'danis'}
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)

#     return Response(serializer.data)



from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscriptionStatus(request):
    #Do logic here for accoutn subscription using the stripe account
    return Response("no SubscriptinStatus yet")



@api_view(['POST'])
def receiveData(request):
    Age = request.data['Age']
    Gender = request.data['Gender']
    Current_weight = request.data['Current_weight']
    Desired_weight = request.data['Desired_weight']
    Diet_restrictions = request.data['Diet_restrictions']
    Disliked_Foods = request.data['Disliked_Foods']
    Preferred_food = request.data['Preferred_food']
    Health_conditions = request.data['Health_conditions']
    Weekly_budget = request.data['Weekly_budget']
    extra_information = request.data['extra_information']
    exercise_frequency = request.data['exercise_frequency']

    content_string = f"Age: {Age}, Gender: {Gender}, Current_weight: {Current_weight}, Desired_weight: {Desired_weight}, Diet_restrictions: {Diet_restrictions}, Disliked_Foods: {Disliked_Foods}, Preferred_food: {Preferred_food}, Health_conditions: {Health_conditions}, Weekly_budget: {Weekly_budget}, extra_information: {extra_information}, exercise_frequency: {exercise_frequency}"

   


   
    #OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY",default='none')
    #OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT",default='none')
    #client = OpenAI(api_key=OPENAI_SECRET_KEY)



       

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_SECRET_KEY')}",
    }

    data = {
        "model": 'gpt-3.5-turbo',
        "messages": [{"role": "user", "content" : f"You are a personal fitnes trainer Trainer, give me a detailed weekly meal plan using the following parameters. Age: {Age}, Gender: {Gender}, Current_weight: {Current_weight}, Desired_weight: {Desired_weight}, Diet_restrictions: {Diet_restrictions}, Disliked_Foods: {Disliked_Foods}, Preferred_food: {Preferred_food}, Health_conditions: {Health_conditions}, Weekly_budget: {Weekly_budget}, extra_information: {extra_information}, exercise_frequency: {exercise_frequency}",}],
        "temperature": 0,
    }

    response = requests.post(os.getenv('OPENAI_ENDPOINT'), headers=headers, data=json.dumps(data))

    if response.status_code == 200:      
        print(response.json())
       # return response.json()["choices"][0]["message"]["content"]
        return Response(response.json(), mimetype="application/json")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")



