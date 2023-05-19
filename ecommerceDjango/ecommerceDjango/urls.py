from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.views.static import serve
from user.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('usuario/', include('user.urls')),
    path('products/', include('products.urls')),
    path('products_viewset/', include('products.routers')),
    path('users_viewset/', include('user.routers')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


'''
a tokenObtain al hacerle una peticion nos retorna un token de acceso y uno de refresco
Refresh refresca el token refresh  que nos  da la  primer ruta y lo asigna como current token

Una peticion a obtainview retorna token access y refresh.
Una peticion a refreshview con el token refresh nos retorna un nuevo access,
un nuevo refresh y envia a la lista negra el primer refresh que le enviamos
Una peticion con access autoriza la peticion 

la blacklist es consultable desde el admin de Django!

'''

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    ]