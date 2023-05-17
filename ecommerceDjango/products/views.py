'''
LO QUE USE UNA PK EN LA URL REQUERE DE UNA QUERY GET
'''


from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import viewsets
from user import Authentication


class ProductViewSet(Authentication,viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True)
    

class MeasureUnitList(generics.ListAPIView): 
#listAPIView se utiliza cuando la view unicamente listara una query
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
       return MeasureUnit.objects.filter(state=True)

'''
A una listAPIView con indicarle la consulta ya es suficiente para que liste 
los objetos que trae dicha query. Es el mismo proceso de cuando usabamos def 
en la view de users, pero de otra forma

'''


class IndicatorList(generics.ListAPIView): 
#listAPIView se utiliza cuando la view unicamente listara una query
    serializer_class = IndicatorSerializer

    def get_queryset(self):
       return Indicator.objects.filter(state=True)



class CategoryProductList(generics.ListAPIView): 
#listAPIView se utiliza cuando la view unicamente listara una query
    serializer_class = CategoryProductSerializer

    def get_queryset(self):
       return CategoryProduct.objects.filter(state=True)


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Producto.objects.filter(state=True)

class ProductDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer
#RetrieveAPIView hace que la view automaticamente funcione para detail
    def get_queryset(self):
       return Producto.objects.filter(state=True)
    
class ProductUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
       return Producto.objects.filter(state=True)

