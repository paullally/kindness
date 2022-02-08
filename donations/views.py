from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .models import Membership, UserMembership, Subscription
from django.contrib.auth.decorators import login_required
from .forms import DonationForm
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
        form = DonationForm()

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
def subscribe(request):
    user_membership = get_membership(request)
    form = DonationForm()

    if request.method == "POST":
        form_data = request.POST
        token = request.POST['stripeToken']
        form = DonationForm(form_data, instance=user_membership)

        if form.is_valid():
            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token
            customer.save()
            form.save()
            select_membership = selected_membership(request)
            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": select_membership.stripe_plan_id},
                ]
            )
            user_membership = get_membership(request)
            user_membership.membership = select_membership
            user_membership.save()

            subscription_id = subscription.id
            sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
            sub.stripe_subscription_id = subscription_id
            sub.active = True
            sub.save()

            try:
                del request.session['selected_membership_type']
            except BaseException:
                pass

            messages.add_message(
                request,
                messages.SUCCESS,
                'Donation Was Updated')
            return redirect('overview')
        else:
            return redirect(reverse('donations'))

    context = {
        'selected_membership': selected_membership,
        'form': form,
    }

    return render(request, 'donations/checkout.html', context)


def overview(request):
    """ This page renders the subscription overview. Renders the information for the user """
    current_membership = get_membership(request)
    subscription = get_subscription(request)
    memberships = Membership.objects.all()

    context = {
        'current_membership': current_membership,
        'subscription': subscription,
        'memberships': memberships,
    }
    return render(request, 'donations/overview.html', context)