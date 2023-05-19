from django.db import models
from simple_history.models import HistoricalRecords
from base.models import BaseModel
from products.models import Producto
from django.core.exceptions import ObjectDoesNotExist

class PaymentType(BaseModel):
    name = models.CharField('Nombre de Medio de Pago', max_length=100)

    class Meta:
        ordering = ['id']
        verbose_name = 'Medio de Pago'
        verbose_name_plural = 'Medio de Pagos'

    def __str__(self):
        return self.name


class Voucher(BaseModel):
    name = models.CharField('Nombre de comprobante de Pago', max_length=100)

    class Meta:
        ordering = ['id']
        verbose_name = 'Comprobante'
        verbose_name_plural = 'Comprobantes'

    def __str__(self):
        return self.name


class ExpenseCategory(BaseModel):
    name = models.CharField('Nombre de Categoría de Gasto', max_length=100)

    class Meta:
        ordering = ['id']
        verbose_name = 'Categoria de Gasto'
        verbose_name_plural = 'Categorias de Gastos'

    def __str__(self):
        return self.name

class Expense(BaseModel):
    date = models.DateField('Fecha de emisión de factura', auto_now=False, auto_now_add=False)    
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('Precio Unitario', max_digits=10, decimal_places=2, default=0)
    voucher_number = models.CharField('Número de comprobante', max_length=50)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'

    def __str__(self):
        return self.voucher_number

class Merma(BaseModel):
    date = models.DateField('Fecha de emisión de Merma', auto_now=False, auto_now_add=False)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.DecimalField('Cantidad', max_digits=7, decimal_places=2)
    lost_money = models.DecimalField('Dinero perdido', max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['id']
        verbose_name = 'Merma'
        verbose_name_plural = 'Mermas'


    def __str__(self):
        return "Merma de {0}".format(self.product.__str__())