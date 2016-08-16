from rest_framework import serializers
from models import Op
import django.contrib.auth


class UserSerializer(serializers.ModelSerializer):
    ops = serializers.PrimaryKeyRelatedField(many=True, queryset=Op.objects.all())

    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active',
                  'date_joined', 'password',)
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'is_active', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class OpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Op
        fields = ('id', 'user', 'script', 'callback_url', 'status', 'info')
        read_only_fields = ('id', 'user', 'status', 'info')

