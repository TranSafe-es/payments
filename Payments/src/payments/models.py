from django.db import models
import uuid
from cards.models import Card


class Payment(models.Model):
    payment_id = models.CharField(max_length=128, default=uuid.uuid4, blank=False, unique=True)
    transaction_id = models.CharField(max_length=128, blank=False)
    buyer_id = models.CharField(max_length=128, blank=False)
    buyer_card = models.ForeignKey(Card, blank=False, null=True, related_name='buyer_card')
    seller_id = models.CharField(max_length=128, blank=False)
    seller_card = models.ForeignKey(Card, blank=False, null=True, related_name='seller_card')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    state = models.CharField(max_length=128, default="Pending", blank=False)
