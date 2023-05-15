from django.urls import path, include
from .views import *
urlpatterns = [

    path('usuario/', user_api_view, name='usuario'),
    path('usuario/<int:pk>/', user_detail_view),
]