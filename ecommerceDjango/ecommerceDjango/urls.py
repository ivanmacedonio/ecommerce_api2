from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('user.urls')),
    path('products/', include('products.urls')),
]
