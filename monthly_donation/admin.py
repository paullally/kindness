from django.contrib import admin

# Register your models here.
from .models import  Donors,  Active, Donation

admin.site.register(Donors)
admin.site.register(Active)
admin.site.register(Donation)
