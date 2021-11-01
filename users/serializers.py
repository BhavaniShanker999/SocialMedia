from django.db.models import fields
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    # media_segment_id = serializers.CharField(max_length= 50,default = "all")

    class Meta:
        model = User
        fields = ('email',
                  'name',
                  'phone',
                  'password'
                  )

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    name=validated_data['name'],
                    phone=validated_data['phone'],
                    password=make_password(validated_data['password']),
                    is_active=1,
                    is_admin=0

                    )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
