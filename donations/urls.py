from django.urls import path
from . import views

urlpatterns = [
   path('plan/', views.donations, name='donations')
]