from django.db import models
from django.core.validators import RegexValidator
import uuid


class Card(models.Model):
    user_id = models.CharField(max_length=128, blank=False)
    card_id = models.CharField(max_length=128, default=uuid.uuid4, blank=False, unique=True)
    alphanumeric = RegexValidator(r'^[0-9]+$', 'Only Numbers')
    number = models.CharField(max_length=16, blank=False, validators=[alphanumeric])
    expire_month = models.IntegerField(blank=False)
    expire_year = models.IntegerField(blank=False)
    cvv2 = models.CharField(max_length=3, blank=False, validators=[alphanumeric])
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=100, blank=False)
    defined = models.BooleanField(blank=False, default=True)
