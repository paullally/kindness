from django.urls import path
from . import views

urlpatterns = [
   path('plan/', views.donations, name='donations'),
   path('checkout/', views.checkout, name='checkout'),
    path('overview/', views.overview, name='overview'),

   
]