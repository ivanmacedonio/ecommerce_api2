from django.contrib import admin
from products.models import *
# Register your models here.


class MeasureUnitAdmin(admin.ModelAdmin): #para que en el form de post podamos ver las 
    #unidades por nombre y no por id 
    list_display = ('id','description')

admin.site.register(MeasureUnit,MeasureUnitAdmin)
admin.site.register(CategoryProduct)
admin.site.register(Indicator)
admin.site.register(Producto)