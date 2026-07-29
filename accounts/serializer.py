from rest_framework import serializers
from .models import CustomUser
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'id', 'first_name', 'last_name', "avatar", 'email', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError({'msg': 'Parollar mos emas'})
        return data

    def validate_username(self, value):
        if len(value) < 4:
            raise ValidationError("Username kamida 4 ta belgidan iborat bo'lishi kerak")
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError("Bu username allaqachon band qilingan")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Bu email bilan allaqachon ro'yxatdan o'tilgan")
        return value

    def validate_first_name(self, value):
        if value and len(value) < 2:
            raise ValidationError("Ism juda qisqa")
        return value

    def validate_last_name(self, value):
        if value and len(value) < 2:
            raise ValidationError("Familiya juda qisqa")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user

    def to_representation(self, instance):
        user = super().to_representation(instance)
        user['status'] = status.HTTP_201_CREATED
        user['msg'] = 'SignUp successful'
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise ValidationError({'msg': 'Login yoki parol xato'})

        if not check_password(password, user.password):
            raise ValidationError({'msg': 'Login yoki parol xato'})

        data['user'] = user
        return data

    def to_representation(self, instance):
        user = instance.get('user')
        refresh = RefreshToken.for_user(user)

        return {
            'messages': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not check_password(attrs.get('old_password'), user.password):
            raise ValidationError({'msg': "Eski parol noto'g'ri"})
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get('new_password'))
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'msg': "Parollar o'zgartirildi",
            'status': status.HTTP_200_OK
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']

    def validate(self, attrs):
        user = self.instance
        username = attrs.get('username', user.username if user else None)
        email = attrs.get('email', user.email if user else None)

        if user and CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            raise ValidationError({'msg': 'Bu username bazada bor'})

        if user and CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise ValidationError({'msg': 'Bu email bazada bor'})

        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance