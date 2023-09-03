from django.shortcuts import render
from .models import User
from .serializer import UserSerializer
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination

# Create your views here.

# Create user
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        # permissions.AllowAny
        permissions.AllowAny
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Create token
        token = Token.objects.create(user=serializer.instance)
        # print(serializer.data)
        return Response(
            data={
                'confirmation_url': reverse('users:activate', kwargs={'token': token.key}, request=request)
            },
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

# Activate user
class ActivateUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # Get token
        token = kwargs.get('token')
        if not token: # If token is not provided
            raise exceptions.AuthenticationFailed('Invalid token')
        # Search for user with token
        user = User.objects.filter(auth_token__key=token).first()
        if not user:
            raise exceptions.AuthenticationFailed('Invalid token')

        user.is_active = True
        user.save()
        return Response(
            {'User Activated'},
            status=status.HTTP_200_OK
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = PageNumberPagination

# Retrieve token
class RetrieveToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Get username and password
        username = request.data.get('username')
        password = request.data.get('password')
        # Search for user
        user = User.objects.filter(username=username).first()
        if not user:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is not active')
        # Get token
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            data={
                'token': token.key
            },
            status=status.HTTP_200_OK
        )

class ResetPassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get user
        user = request.user
        # Get password
        password = request.data.get('password')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')
        # Get new password
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response(
            data={
                'message': 'Password updated'
            },
            status=status.HTTP_200_OK)