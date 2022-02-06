from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings


from .forms import OrderForm
from .models import Order, OrderLineItem
from shop.models import Product
from bag.contexts import bag_contents





from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


import stripe
import json

def checkout(request):
    """
    render the checkout page. Willl also process the checkout post request & fullfill this. 
    If information is rendered incorrectly, it will redirect the user back to the bag 
    and displays an error message prompting users to try again.
    If all completed successfully this will direct the user to the checkout success view.
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    item = CurrentItem.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        item=item,
                        quantity=item_data,
                    )
                    order_line_item.save()

                except CurrentItem.DoesNotExist:
                    messages.error(
                        request, ("One of the products in your bag wasn't found in our database. "
                                  "Please call us for assistance!"))
                    order.delete()
                    return redirect(reverse('bag.html'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse(
                    'checkout_success',
                    args=[
                        order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('shop'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)
