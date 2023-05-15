from .models import *
from rest_framework import serializers

class MeasureUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasureUnit
        exclude = ('state','deleted_date','modified_date',)


class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProduct
        exclude = ('state','deleted_date','modified_date',)

class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        exclude = ('state','deleted_date','modified_date',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        exclude = ('state','deleted_date','modified_date','created_date',)

    def to_representation(self,instance):
        return {
            'id' : instance.id,
            'description' : instance.description,
            'image': instance.image if instance.image != '' else '', #como en json se espera que imagen retorne algo, para
            #no tumbar el programa hacemos la validacion, donde nos aseguramos que retorne algo 
            #aunque sea una cadena vacia

            #serializamos las claves foraneas para que en el get no muestre solo su id
            'measure_unit': instance.measure_unit.description,
            'category_product':instance.category_product.description 
            }

        