from django.shortcuts import render
from rest_framework.response import Response
from .serializer import SignUpSerializer, LoginSerializer, PasswordChangeSerializer, ProfileUpdateSerializer
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            'msg': 'Profile info',
            'status': status.HTTP_200_OK,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        })


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PasswordChangeSerializer(
            instance=request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenRefresh(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh = request.data.get('refresh')


        if not refresh:
            raise ValidationError({'msg': 'Refresh token yuborilmadi'})


        refresh_token = RefreshToken(refresh)

        return Response({
            'access': str(refresh_token.access_token)
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"msg": "Tizimdan muvaffaqiyatli chiqdingiz"},
            status=status.HTTP_200_OK
        )

