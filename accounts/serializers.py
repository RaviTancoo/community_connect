from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type', 'location']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            location=validated_data.get('location', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# THIS MUST EXIST for your tests
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = [
            'username',  # can't change username
            'user_type',  # can't change user type
            'email',      # optionally make email read-only
            'password'
        ]
