from rest_framework.routers import DefaultRouter
from .views import ProductViewSet


router = DefaultRouter()

router.register(r'products', ProductViewSet)

#en las '' indicamos el nombre de la ruta que tendra en el navegador la viewset

urlpatterns = router.urls

#urlpatterns sirve para que django reconozca una ruta, ya sea url o router

#el router debe ser cargado en el archivo MAIN de urls
# path('products_viewset/', include('products.routers')),

