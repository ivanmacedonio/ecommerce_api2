from .models import * 
from rest_framework import serializers

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        exclude = (
            "state",
            "created_date",
            "deleted_date",
            "modified_date",
        )

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id','ruc','business_name','address')

class SupplierRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = (
            "state",
            "created_date",
            "deleted_date",
            "modified_date",
        )

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('id','name')


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id','name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id','name')


