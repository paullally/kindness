from django.db.models.signals import post_save

from django.conf import settings
from django.db import models

DONATION_AMOUNT = (
    ('0', '0'),
    ('10', '10'),
    ('20', '20'),
    ('50', '50'),
)
