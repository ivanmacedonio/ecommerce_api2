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
        exclude = ('state','deleted_date','modified_date',)

        