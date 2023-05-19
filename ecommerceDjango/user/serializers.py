from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name')
        
    def to_representation(self, instance): #podemos serializar todos los campos pero gracias a esta funcion elegir cual ver en el get
        return {
            'id'  : instance.id,
            'username' : instance.id,
            'password' : instance.password
        }
    
class PassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6)
    password2 = serializers.CharField(max_length=128, min_length=6)

    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'passoword': 'No coinciden las password'})
        return data
    
class UserlISTSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
    def to_representation(self, instance): #podemos serializar todos los campos pero gracias a esta funcion elegir cual ver en el get
        return {
            'id'  : instance.id,
            'username' : instance.id,
            'password' : instance.password
        }
#indica en que forma se muestra la info serializada cuando se la 
#llama en una query get 

class UserTokenSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    pass



