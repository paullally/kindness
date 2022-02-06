from django.db.models.signals import post_save

from django.conf import settings
from django.db import models

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

DONATION_AMOUNTS = (
    ('0', 'reg'),
    ('5', '5'),
    ('10', '10'),
    ('20', '20'),
)


# Donation type View for DB admin
class Donation(models.Model):
    Donation_type = models.CharField(
        choices=DONATION_AMOUNTS,
        default='Free',
        max_length=200, null=False, blank=False)
    price = models.IntegerField(default=15)
    description = models.TextField()
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.Donation_type


class Donors(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    Donation = models.ForeignKey(
        Donation, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=254, null=False)
    phone_number = models.CharField(max_length=30, null=False)
    postcode = models.CharField(max_length=500, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False)
    street_address1 = models.CharField(max_length=80, null=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True)
    country = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.user.username


def create(
        sender, instance, created, *args, **kwargs):
    user_Donation, created = Donors.objects.get_or_create(
        user=instance)

    if user_Donation.stripe_customer_id is None or user_Donation.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        free_Donation = Donation.objects.get(Donation_type='Free')
        user_Donation.stripe_customer_id = new_customer_id['id']
        user_Donation.Donation = free_Donation
        user_Donation.save()


post_save.connect(create,
                  sender=settings.AUTH_USER_MODEL)


class Active(models.Model):
    user_Donation = models.ForeignKey(
        Donors, on_delete=models.CASCADE)
    stripe_Active_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user_Donation.user.username