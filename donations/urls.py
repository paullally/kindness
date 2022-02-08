from django.urls import path
from . import views

urlpatterns = [
   path('', views.overview, name='overview'),
   path('plan/', views.donations, name='donations'),
   path('checkout/', views.checkout, name='checkout'),
   
   
]