from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate


class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'date_of_birth', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Password and confirm password do not match.")
        return data

    def create(self, validated_data):

        validated_data.pop('confirm_password')
        return Account.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password', None)
    #     confirm_password = validated_data.pop('confirm_password', None)

    #     if password and confirm_password:
    #         if password != confirm_password:
    #             raise serializers.ValidationError("Passwords do not match")

    #     user = super().update(instance, validated_data)
    #     if password:
    #         user.set_password(password)
    #         user.save()
    #     return user

class AuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                attrs['user'] = user
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return attrs
