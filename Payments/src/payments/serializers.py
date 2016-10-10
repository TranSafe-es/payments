from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('user_id1', 'user_id2', 'transaction_id', 'amount', 'description')

