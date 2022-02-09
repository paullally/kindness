from django.urls import path
from . import views

urlpatterns = [
   path('', views.overview, name='overview'),
   path('plan/', views.donations, name='donations'),
   path('subscribe/', views.subscribe, name='subscribe'),
   path('cancel/', views.cancelSubscription, name='cancelSubscription'),
   path('choice/', views.loggedout, name='loggedout'),
   
   
]