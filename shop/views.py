from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.
def all_products(request):
    """show all products """
    products = Product.objects.all()
    

    context = {
        'products':products,

    }

    
    return render(request,'shop/shop.html', context)

def product_detail(request, product_id):

    """show single product """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product':product,

    }
    return render(request,'shop/shop_detail.html', context)
