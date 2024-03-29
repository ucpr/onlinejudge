from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash

from .models import Account, AccountManager


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return Account.objects.create_user(request_data=validated_data)

