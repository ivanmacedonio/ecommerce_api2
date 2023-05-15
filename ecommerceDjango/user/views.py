from .models import *
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response  import Response
from rest_framework.decorators import api_view

@api_view(['GET','POST'])#darle decorador apiview indicando  que metodo aceptara
#le da el formato valido para trabajar como una API, pues lo valida para 
#recibir peticiones http
def user_api_view(request):

    if request.method == 'GET':
        users = User.objects.all()
        users_serializer =  UserSerializer(users, many=True)#con many el serializador sabe que no recib 1 elemento,sino una lista
        return Response(users_serializer.data,status=status.HTTP_200_OK)#retorna un json con la data de la query
    
    elif request.method == 'POST':
        users_serializer = UserSerializer(data = request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
def user_detail_view(request,pk):
    if request.method == 'GET':
        if pk is not None:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        user = User.objects.get(id=pk)
        user_serializer = UserSerializer(user,data=request.data)#al enviarle la instancia user, entiende que la informacion que se encontraba
        #en user debe ser remplazada por la data que le enviamos por parametro
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'message': 'Usuario eliminado correctamente!'})
    
    

