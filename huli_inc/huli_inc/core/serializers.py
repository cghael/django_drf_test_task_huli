from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)

    class Meta:
        # fields = '__all__'
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email')
        model = User
