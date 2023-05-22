from .models import *
from rest_framework import serializers


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        exclude = (
            "state",
            "deleted_date",
            "modified_date",
        )


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        exclude = (
            "state",
            "deleted_date",
            "modified_date",
        )


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = (
            "state",
            "deleted_date",
            "modified_date",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        exclude = (
            "state",
            "deleted_date",
            "modified_date",
            "created_date",
        )

#la funcion de estas validaciones, es que si no se envia el campo measure o cat 
#que retorne un response, pues el null False indicado en el model no retorna ningun
#mensaje al frontend.

#Estas dos validaciones retornar response en el caso de enviar el campo VACIO
    def validate_measure_unit(self,value): 
        if value == '' or value  == None:
            raise serializers.ValidationError({'error':'Debe ingresar una unidad de medida'})
        return value

    def validate_category_product(self,value): #indicamos que este dato sera obligatorio pero desde el serializer, no el model
        if value == '' or value  == None:
            raise serializers.ValidationError({'error':'Debe ingresar una categoria'})
        return value

#Estas dos validaciones retornar response en el caso de NO enviar el campo
    def validate(self,data):
        if 'measure_unit' not in data.keys():
            raise serializers.ValidationError({'error':'Debe ingresar una Unidad de medida'})
        if 'category_product' not in data.keys():
            raise serializers.ValidationError({'error':'Debe ingresar una categoria '})

        return data

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "stock": instance.stock.get('quantity__sum',0) if instance.stock.get('quantity__sum') is not None else 0,
#toma el campo quantity, donde su clave es quantity__sum, (nombre de campo __ operacion), por defecto es 0
            "description": instance.description,
            "image": instance.image.url if instance.image!= '' else '',
            "measure_unit": instance.measure_unit.description,
            "category_product": instance.category_product.description,
        }
    



       