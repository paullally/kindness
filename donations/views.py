from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .models import Membership, UserMembership, Subscription
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from django.contrib import messages


import stripe

stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY

@login_required()
def get_membership(request):
    membership = UserMembership.objects.filter(user=request.user)
    if membership.exists():
        return membership.first()
    return None

@login_required()
def get_subscription(request):
    subscription = Subscription.objects.filter(
        user_membership=get_membership(request))
    if subscription.exists():
        user_subscription = subscription.first()
        return user_subscription
    return None


@login_required()
def selected_membership(request):
    membership_type = request.session['selected_membership_type']
    membership = Membership.objects.filter(
        membership_type=membership_type)
    if membership.exists():
        return membership.first()
    return None



@login_required()
def donations(request):

    if request.method == "POST":
        selected_membership_type = request.POST.get('membership_type')
        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)
        request.session['selected_membership_type'] = selected_membership.membership_type
        form = SubscriptionForm()

        context = {

            'selected_membership': selected_membership,
            'stripe_public_key': stripe_public_key,
            'form': form
        }
        return render(request, 'donations/checkout.html', context)


    memberships = Membership.objects.all()
    current_membership = get_membership(request)
    users_membership = str(current_membership.membership)
    subscription = get_subscription(request)
    context = {
        'memberships': memberships,
        'users_membership': users_membership,
        'subscription': subscription,
    }

    return render(request, 'donations/donations.html', context)


@login_required()
def checkout(request):
    return render(request, 'donations/checkout.html', context)