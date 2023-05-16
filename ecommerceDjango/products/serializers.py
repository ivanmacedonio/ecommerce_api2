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

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "description": instance.description,
            "measure_unit": instance.measure_unit.description,
            "category_product": instance.category_product.description,
        }
