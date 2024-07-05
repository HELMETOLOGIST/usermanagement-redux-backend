from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAccount

User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError({'password': serializer_errors['non_field_errors']})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser'] 
    
class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'email', 'is_superuser', 'profile_image']

    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        instance = super().update(instance, validated_data)
        if profile_image:
            instance.profile_image = profile_image
            instance.save()
        return instance

