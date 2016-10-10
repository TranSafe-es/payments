from django.db import models
import uuid
from cards.models import Card


class Payment(models.Model):
    payment_id = models.CharField(max_length=128, default=uuid.uuid4, blank=False, unique=True)
    transaction_id = models.CharField(max_length=128, blank=False)
    user_id1 = models.CharField(max_length=128, blank=False)
    card_1 = models.ForeignKey(Card, blank=False, null=True, related_name='buyer_card')
    user_id2 = models.CharField(max_length=128, blank=False)
    card_2 = models.ForeignKey(Card, blank=False, null=True, related_name='seller_card')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    description = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, default="Pending", blank=False)
