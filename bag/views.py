from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required()
def view_bag(request):
    """ renders bag """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(view_bag)


@login_required()
def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
    else:
        bag.pop(item_id)

    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


@login_required()
def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    bag = request.session.get('bag', {})
    try:
        bag.pop(item_id)

        request.session['bag'] = bag

        return HttpResponse(status=200)
    except Exception as e:
        messages.add_message(request, messages.SUCCESS, 'error! Try again!')
        return HttpResponse(status=500)
