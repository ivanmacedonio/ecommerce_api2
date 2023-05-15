from rest_framework import generics
from .models import *
from .serializers import *

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


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Producto.objects.filter(state=True)
    
    