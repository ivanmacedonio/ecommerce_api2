from django.shortcuts import render
from .models import *
from .serializers import * 
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from products.models import Producto
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime

def format_date(date): #para que el front reconozca la fecha correctamente 
    date = datetime.strptime(date, '%d/%m/%Y')
    date = f"{date.year}-{date.month}-{date.day}-"
    return date

class ExpenseViewSet(viewsets.GenericViewSet):
    serializer_class = ExpenseSerializer

    @action(methods=['get'], detail=False, url_path='search_supplier')
    #detail true se usa cuando retornamos SOLO UN objeto,
    #false se usa cuando retornamos una lista de objetos
    def buscar_proveedor(self,request):
        ruc_or_business_name = request.query_params.get('ruc_or_business_name', '')
        '''
        En el input de la interfaz en el frontend el input donde se escribe para buscar proveedor esta bajo la id ruc_or_business_name,
        En este caso request.query_params.get lo que hace es traer solo una parte de la consulta, en este caso, del request entero solo rescata
        lo que venga bajo la id de ruc_or_business_name
        '''
        supplier = Supplier.objects.filter(
            Q(ruc__iexact=ruc_or_business_name) | #busca una coincidencia entre los ruc guardados en la base de datos y lo que se almaceno en la variable
            #en este caso iexact hace que no importen las mayusculas. Si en la base de datos 
            #dice Plomeria y en el request llego plomeria, lo identifica igual
            Q(business_name__iexact=ruc_or_business_name)
        ).first()

        '''Q se importa desde django y sirve para hacer una consulta con varios
        argumentos clave. En este caso Q es QUERY. En supplier se almacena el resultado 
        de una consulta que busca 2 argumentos en una misma consulta, pues 
        no sabemos si el proveedor se registro con nombre de negocio o ruc, asique 
        buscamos las dos. Si en la base de datos encuentra una ruc que coincida con 
        ruc_or_business_name, la guarda en supplier con el first. En cambio si encuentra
        un nombre de negocio lo almacena tambien en esa variable y cierra con first'''
        
        if supplier:
            supplier_serializer = SupplierSerializer(supplier)
            return Response(supplier_serializer.data,status=status.HTTP_200_OK)
        return Response({'mensaje':'No se ha encontrado un proveedor'},status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'],detail=False, url_path='create_supplier')
    def crear_proveedor(self,request):
        data_supplier = request.data
        data_supplier = SupplierRegisterSerializer(data_supplier)
        if data_supplier.is_valid():
            data_supplier = data_supplier.save()
            return Response({'message': 'Proveedor registrado correctamente!',
                             'supplier': data_supplier.data},status=status.HTTP_201_CREATED)
        return Response({'error': data_supplier.errors},status=status.HTTP_400_BAD_REQUEST)
    
    '''En el formulario de crear factura, falta hacer la relacion con la tabla
    de productos,tipo de comprobante y medio de pago, para que salgan en el acordeon
    o menu desplegable para seleccionarlos. Para eso los traemos con get '''


#estas funciones  hacen que el acordeon del formulario muestre los productos etc y asi seleccionarlos 
    @action(methods=['get'],detail=False)
    def get_vouchers(self,request):
        data  = Voucher.objects.filter(state=True).order_by('id')
        data =  VoucherSerializer(data,many=True).data
        return Response(data)
    
    @action(methods=['get'],detail=False)
    def get_payment_type(self,request):
        data  = PaymentType.objects.filter(state=True).order_by('id')
        data =  PaymentTypeSerializer(data,many=True).data
        return Response(data)
    
    @action(methods=['get'],detail=False)
    def get_products(self,request):
        data  = Producto.objects.filter(state=True).order_by('id')
        data =  ProductSerializer(data,many=True).data
        return Response(data)
    
    def format_data(self,data):
        data['date'] =format_date(data['date'])
        return data

    def create(self,request): #la logica para registrar la factura
        data = request.data
        
#debemos rescatar el usuario que hace la peticion create para saber quien lo subio

        JWT_authenticator = JWTAuthentication()
        #decode del token current user, retorna el usuario y el token

        user, _ = JWT_authenticator.authenticate(request)
        #almacenamos solo el user, el token no lo necesitamos por eso la _

        data['user'] = user.id #obtenemos el id del usuario que hizo la creacion

        serializer =self.serializer_class(data=data)

        data['date'] = self.format_data(data['date'])
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Factura registrada correctamente!'}
                            ,status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Error en la crecion de la factura'},
                            status=status.HTTP_400_BAD_REQUEST)


        


    
    
    
