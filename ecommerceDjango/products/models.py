from django.db import models
from base.models import BaseModel
from simple_history.models import HistoricalRecords


class MeasureUnit(BaseModel): #indicamos que hereda los campos del modelo padre
    description = models.CharField(max_length=50,blank=False,null=False,unique=True)
    historical = HistoricalRecords()
    #estas propiedades hacen que el historical acceda a los usuarios desde un 
    #model que no es el de User

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de medida'

    
    def __str__(self):
        return self.description


class CategoryProduct(BaseModel):
    description = models.CharField(max_length=50, unique=True, blank=False, null=False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Categoria de producto'
        verbose_name_plural = 'Categorias de productos'

    
    def __str__(self):
        return self.description
    
#Este model sirve para indicar si hay descuento o no

class Indicator(BaseModel):
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct,on_delete=models.CASCADE, verbose_name='Indicadorde oferta')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'indicador de oferta'
        verbose_name_plural = 'Indicadores de ofertas'

    def __str__(self):
        return f'Oferta de la categoria{self.category_product}: {self.descount_value}'

class Producto(BaseModel):
    name = models.CharField(unique=True, blank=False, null=False,max_length=150)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='products/',blank=True, null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, null=True)
    measure_unit = models.ForeignKey(MeasureUnit,on_delete=models.CASCADE,null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Producto' #nombre que aparece en el admin o la bbdd
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.name} -- {self.description}'
    
