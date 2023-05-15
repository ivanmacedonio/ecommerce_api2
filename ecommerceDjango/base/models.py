from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.BooleanField('Estado', default=True)
    created_date= models.DateField('Fecha de creacion', auto_now=False,auto_now_add=True)
    modified_date= models.DateField('Fecha de modificacion', auto_now=True, auto_now_add=False)
    deleted_date = models.DateField('Fecha de eliminacion', auto_now=True, auto_now_add=False)
#auto_now actualiza el campo cada vez que se ejecute el save, 
#mientras que auto_now_add actualiza el campo solo en el momento que se crea 
#la instancia 
    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'
'''
El abstract = True hace que django reconozca este modelo como modelo padre,
donde su unica funcion es hacer que otros modelos hereden su sintaxis, los 
modelos hijos.  Como su funcion es ser una base para el resto,django no le crea 
una tabla en la base de datos
'''

