from .models import *
from rest_framework import status
from .serializers import *
from rest_framework import viewsets
from rest_framework.response  import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

'''
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
    
    

#Ｔｏｋｅｎｓ／ｌｏｇｉｎ SIN JWT


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
        
        


class UserToken(APIView): #valida el token
    def get(self,request,*args,**kwargs):
        
        try:
            user_token,_ = Token.objects.get_or_create( #como getorcreate retorna 2 valores y solo quiero uno, indico _
                user=self.user) #extrae del login
            user = UserTokenSeralizer(self.user)
            return Response({
                'token':user_token.key,
                'user' : user.data
            })
        except:
            return Response({'error' : 'Credenciales enviadas incorrectas'},
                            status=status.HTTP_400_BAD_REQUEST)
        

'''
#Ｔｏｋｅｎｓ／ｌｏｇｉｎ CON SIMPLE JWT

class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get('username','')
        password = request.data.get('password','')
        user = authenticate(
            username = username,
            password = password
        ) #authenticate retorna true o false si existe el user  y pass que le enviamos

        if user:
            login_serializer = self.serializer_class(data=request.data) #serializa el token
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user) #serializa el user
                return Response({
                    'token':login_serializer.validated_data.get('access'),
                    'refresh': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesion exitoso'
                },status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o user incorrectos'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o user incorrectos!'},status=status.HTTP_400_BAD_REQUEST)
    
class Logout(GenericAPIView):
    def post(self,request,*args,**kwargs):
        user = User.objects.filter(id=request.data.get('user',0))
        if user.exists():
            RefreshToken.for_user(user.first())#actualiza el token del usuario que le enviamos
            return Response({'message':'Sesion cerrada correctamente'}
                            ,status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario!'},status=status.HTTP_400_BAD_REQUEST)
#refrescar el token y eliminar el anterior es un metodo de login 
#para eliminar o invalidar el token anterior, debemos agregarlo a la blacklist

class UserViewSet(viewsets.GenericViewSet): #es un viewset que no se basa en un modelo, sino que trae getobject y getqueryset, aunque no automatiza el CRUD como modelviewset
#al ser generico, los metodos http deben ser definidos explicitamente

    serializer_class = UserSerializer
    list_serializer_class= UserlISTSerializer
    queryset = None #genericviewset si recibe una consulta, la carga en esta 
    #variable automaticamente

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True)
        return self.queryset
    
    def get_object(self,pk): #basado en un pk traer el objeto o un raise
        return self.serializer_class().Meta.model.objects.get(id=pk)
   
#Colocarle el decorador action a una funcion dentro de una clase, hace que
#dicha funcion sea una ruta dentro de la ruta de la clase. En este caso podemos 
#acceder a dicha funcionalidad accendiendo primero a la ruta de UserViewSet/change_password    
    @action(detail=True,methods=['post']) #detail indica que sera una ruta dentro de otra
    def change_password(self,request,pk=None):
        user = self.get_object(pk)
        pass_serializer = PassSerializer(data=request.data)
        if pass_serializer.is_valid(): #la validacion esta sobreescrita en el serializer, pues no usamos modelserializer, ya que serializamos una instancia no una tabla
            user.set_password(pass_serializer.validated_data['password'])
            user.save()
            return Response({'message': 'Pass updated!'},status=status.HTTP_200_OK)
        return Response({'message': 'Error en la validacion'},
                        status=status.HTTP_400_BAD_REQUEST)
#sirve para asignarle a los viewsets funciones que no sean las que trae definidas 
#por defecto, que son list,create,delete,etc... 
    def list(self,request):     
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users,many=True)
        return Response(users_serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario registrado correctamente'},status=status.HTTP_201_CREATED)
        return Response({'message': 'Error en la creacion del usuario'},status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        user = self.get_object(pk)
        if user is not None:
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el user'},status=status.HTTP_404_NOT_FOUND)
    

    def update(self,request,pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data) #usamos un serializer especifico ya que si usamos el serializer general, este nos va a pedir todos los campos y en el update generalmente se actualizan unos pocos campos, no todos
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario updateado!'},
                            status=status.HTTP_200_OK)
        return Response ({'message': 'Hay errores en la actualizacion',
                         'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self,request,pk=None):
        user = self.get_object(pk)
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        #update retorna la cantidad de filas afectadas, en este caso si se elimino correctamente debe retornar un 1
        if user_destroy == 1:
            return Response({'message':'Usuario eliminado correctamente'})
        return Response({'message': 'No existe un usuario con este id'},status=status.HTTP_404_NOT_FOUND)
    