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
        membership=getmembership(request))
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