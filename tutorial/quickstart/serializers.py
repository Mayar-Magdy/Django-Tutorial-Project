from django.contrib.auth.models import User , Group
from rest_framework import serializers

# creating a new user with [password hashing]
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' ,'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name'] 


class GroupCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)