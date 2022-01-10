from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,on_delete=models.SET_NULL)
    pid = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name