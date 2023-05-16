from django.contrib import admin
from django.urls import path, include
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('usuario/', include('user.urls')),
    path('products/', include('products.urls')),
    path('products_viewset/', include('products.routers')),
]
