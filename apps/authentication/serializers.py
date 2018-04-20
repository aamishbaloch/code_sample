from rest_framework import serializers
from django.contrib.auth import get_user_model

from libs.jwt_helper import JWTHelper

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'groups', 'user_permissions', 'verification_code')

    def to_internal_value(self, data):
        """
        adding customer role to User Model
        """
        data = super(UserSerializer, self).to_internal_value(data)
        data['role'] = User.Role.CUSTOMER
        return data

    def get_extra_kwargs(self):
        extra_kwargs = super(UserSerializer, self).get_extra_kwargs()
        if self.instance is None:
            kwargs = extra_kwargs.get('password', {})
            kwargs['required'] = True
            extra_kwargs['password'] = kwargs
        else:
            kwargs = extra_kwargs.get('password', {})
            kwargs['required'] = False
            extra_kwargs['password'] = kwargs
            kwargs = extra_kwargs.get('phone', {})
            kwargs['read_only'] = True
            extra_kwargs['phone'] = kwargs

        return extra_kwargs

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserTokenSerializer(UserSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, doctor):
        user = JWTHelper.encode_token(doctor)
        return user
