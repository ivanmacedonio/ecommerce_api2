from .models import *
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response  import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from datetime import datetime

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
    
    

#Ｔｏｋｅｎｓ／ｌｏｇｉｎ

class Login(ObtainAuthToken): # es una vista apiview que define un post y trae un serializador para el login

    def post(self,request,*args,**kwargs):
        login_serializer = self.serializer_class(data= request.data, context = {'request' : request})

        if login_serializer.is_valid():#si el user y pass coinciden con uno registrado en la bbdd pasa la validacion
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created= Token.objects.get_or_create(user = user) #trae el token para user, y si no existe se lo crea
#si crea el token lo guarda en created, si ya existia en token           
                user_serializer = UserTokenSeralizer(user)
                if created:
                    return Response({
                        'token' : token.key,
                        'user': user_serializer.data,
                        'message': 'Sesion iniciada,Token creado!'
                    },status=status.HTTP_201_CREATED)
                else:
#si se loguea y ya tiene token, debemos eliminar el que tenia antes y crearle uno nuevo
#pues si inicia sesion de 2 lugares diferentes no pueden circular 2 token para el mismo
#usuario
                    all_sessions =  Session.objects.filter(expire_date__gte = datetime.now()) #trae  a todas las sesiones que expiran tiempo despues de la ejecucion, es decir a todas las sesiones que aun no expiran
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded() #decodifica para poder interpretarla
                            if user.id == int(session_data.get('_auth_user_id')): #si el id del current user coincide con la id de algun  usuario con sesion abierta, se la cierra
                                session.delete()
                    token.delete()
#sin token, no hay peticiones, sin session, lo bota al login
                    token = Token.objects.create(user=user)
                    return Response({
                        'token' : token.key,
                        'user': user_serializer.data,
                        'message': 'Sesion iniciada,Token creado!'
                    },status=status.HTTP_201_CREATED)
            else:
                return Response ({'error':'Validacion erronea!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:      
            return Response ({'message':'Validacionerronea!'}, status=status.HTTP_400_BAD_REQUEST)
        

class Logout(APIView):
    def get(self,request,*args,**kwargs):
        try:
            token = request.GET.get('token')
            user = Token.objects.get(key=token)
            if token:
                user = token.user
                all_sessions =  Session.objects.filter(expire_date__gte = datetime.now()) #trae  a todas las sesiones que expiran tiempo despues de la ejecucion, es decir a todas las sesiones que aun no expiran
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded() #decodifica para poder interpretarla
                        if user.id == int(session_data.get('_auth_user_id')): #si el id del current user coincide con la id de algun  usuario con sesion abierta, se la cierra
                            session.delete()

                token.delete()
                return Response({'messsage': 'Token y sesion eliminados!'},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'error': 'No se ha encontrado un Token asignado!'}, status=status.HTTP_409_CONFLICT)
        
        

