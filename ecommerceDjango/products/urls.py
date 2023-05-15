from  django.urls import path,include
from .views import *
urlpatterns = [
    path('measure_unit/', MeasureUnitList.as_view(),name='measure_unit' ),
    path('indicator/', IndicatorList.as_view(),name='indicator' ),
    path('category_product/', CategoryProductList.as_view(),name='category_product' )
]
