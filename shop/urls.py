from django.urls import path
from . import views
urlpatterns = [
    path('',views.all_products, name='shop'),
     path('',views.product_detail, name='product_detail'),
]
