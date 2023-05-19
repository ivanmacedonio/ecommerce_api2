'''
LO QUE USE UNA PK EN LA URL REQUERE DE UNA QUERY GET
'''


from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response  import Response
from rest_framework import status

#para modificar el request
def validate_files(request,field,update=False):
    request=request.copy() #copiamos la data del request

    if update:
        if type(request[field]) == str:
            request.__delitem__(field) 
    else:
        if type(request[field]) == str: 
            request.__setitem__(field,None)
#si  nos llega undefined o un str, al campo que le indique (field), le asigne un none 
#en vez de undefined
    return request #retornamos la COPIA, pues el original es inmutable

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    #permission_classes=  (IsAuthenticated,) #Para acceder a esta view,se requiere estar autenticado, es decir tener un token
    queryset = ProductSerializer.Meta.model.objects.filter(state=True)
#la auth solo es necesaria para esta view, si la codeo en settings todas las 
#vistas tendran autenticacion
    def create(self,request):
#la interfaz le asigna "undefined" a image si no se envia nada, asique validamos
#request data es inmutable, no podemos modificarlo, a no ser que implementemos lo siguiente

        data=validate_files(request.data,'image')
        serializer =  self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente'},
                            status=status.HTTP_201_CREATED)
        return Response({'message':'error en la creacion'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        
        if self.get_queryset(pk):
            data = validate_files(request.data,'image',True)
            product_serializer  =self.serializer_class(self.get_queryset(pk), data=data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'message':'actualizado'}, status=status.HTTP_200_OK)
            return Response({'message': 'Error en el update'},status=status.HTTP_400_BAD_REQUEST)
        
    

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

