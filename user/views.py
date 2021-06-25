from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .send_mail import send_confirmation_email, send_reset_password
from .serializers import PassResetApiSerializer, CreateNewPassSerializer

User = get_user_model()


class RegisterApiView(APIView):

    def post(self, request):
        serializer = serializers.RegisterApiSerializer(data=request.data)
        print(f'serializer: {serializer}')
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            print(f'user: {user}')
            if user:
                send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Successfully activated'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class PassResetApiView(APIView):
    def post(self, request):
        serializer = PassResetApiSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data.get('email'))
            user.is_active = False
            user.create_activation_code()
            user.save()
            send_reset_password(user)
            return Response('Check your email', status=200)
        return Response({'msg': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class NewPasswordApiView(APIView):
    def post(self, request):
        serializer = CreateNewPassSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You have successfully changed password!', status=200)