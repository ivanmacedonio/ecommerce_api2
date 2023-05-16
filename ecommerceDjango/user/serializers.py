from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
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





