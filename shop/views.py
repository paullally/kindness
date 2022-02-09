from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product
from django.contrib.auth.decorators import login_required


@login_required()
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('shop'))

            queries = Q(
                name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'shop/shop.html', context)


@login_required()
def product_detail(request, product_id):
    """show single product """
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.all()
    context = {
        'products': products,
        'product': product,

    }
    return render(request, 'shop/shop_detail.html', context)
