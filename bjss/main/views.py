from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
# auth_app/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render, redirect
from django.contrib import messages
def index(request):
    return render(request, 'main/index.html')

@swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={201: "User registered successfully!", 400: "Invalid data"}
)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def option_view(request):
    return render(request, 'main/options.html')
@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={200: "Login successful!", 401: "Invalid username or password.", 400: "Invalid data"}
)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('option')
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

