#En este archivo vamos a codear la autenticacion de las rutas  

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.exceptions  import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from  rest_framework.renderers import JSONRenderer
from rest_framework import status





class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False #debemos retornarle al frontend una variable para que sepa 
    #cuando el token expiro, asi deniega solicitudes
#------------------------------------CALCULO---------------------------------------------------------------------------

    def expires_in(self,token): #calcula el tiempo que falta para que el token expire
        time_elapsed = timezone.now() - token.created #created es el campo del token que almacena el  momento en el que se creo el token
        #creamos la variable estatica en settings
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self,token): #indica si el token expiro o no
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self,token): #retorna el valor de la funcion anterior, indicando si expiro o no
        is_expire =   self.is_token_expired(token)
        if is_expire:
            self.expired = True
            token.delete()
            token = Token.model.objects.create(user = token.user)
        return is_expire,token
    
#------------------------------------CALCULO---------------------------------------------------------------------------
    
    def authenticate_credentials(self, key):
        message,token,user= None,None,None
        try:
            token = Token.model.objects.get(key=key)
            user = token.user
        except Token.model.DoesNotExist:
            message = 'token invalido!'
            self.expired = True
        if token is not None:
            if not token.user.is_active: #si el token es none, no puede obtener el is_active
                message = 'Usuario no activo o eliminado!'     
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message= 'Su token ha expirado!'

        return (user,token,message,self.expired)
    

class Authentication(object):
    user = None
    user_token_expired = False

    def get_user(self,request): #obtiene el token del usuario
        token = get_authorization_header(request).split() #retorna el header del token donde se halla la autorizacion 
        if token:
            try: #si existe la autorizacion..
                token = token[1].decode() #cuando se envian los token, la posicion 0 es la palabra token y la 1 es el token en si, con el decode obtenemos los datos encriptados en ese token
            except:
                return None
            
            token_expire = ExpiringTokenAuthentication()
            user,token,message,self.user_token_expired = token_expire.authenticate_credentials(token)
            if user != None and token !=None:
                self.user = user
                return user
            return message
        return None

    
    def dispatch (self,request,*args,**kwargs): #sobrescribimos el dispatch xq es la primr funcion que se ejecuta llamando a una  clase asique la usamos para definir parametros o funciones de entrada
        user = self.get_user(request) #la funcion le carga un  message si algo salio mal y un usuario si todo salio bien
        if user is not None: #si encontro un token en la peticion
            
            if type(user)  == str: #si get_user le retorno un mensaje, significa que hubo error
                response= Response({'error':user,
                                    'expired': self.user_token_expired},
                                    status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response
            
            if not self.user_token_expired:
                return super().dispatch(request,*args,**kwargs)#si retorno un user, la view SE EJECUTA
        
        response= Response({'error':'No se enviaron las credenciales', 
                            'expired': self.user_token_expired},status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response

'''
El dispatch es lo primero que se ejecuta cuando llamamos a una clase en una view
en este caso antes de ejecutar el dispatch, es decir antes de ejecutar la view, 
se hace una validacion de token. Si se pasa la validacion la view se ejecuta, sino no
Tambien debemos sobreescribir el Response al estar en el dispatch

-Response
los response son esenciales para que el frontend sepa lo que esta sucendiendo,
para asi poder trabajar correctamente. Si el token es invalido, debemos enviar un 
response que indique que el token no es valido, el response es nuestra comunicacion con 
el front, recordemos que ellos no tienen nuestro codigo
Por ejemplo, enviar expired y la variable que indica true o false, ellos lo ven 
como expired : True, eso es informacion valiosa 
'''