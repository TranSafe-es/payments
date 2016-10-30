from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    callback = serializers.CharField(max_length=256)

    class Meta:
        model = Payment
        fields = ('user_id1', 'user_id2', 'transaction_id', 'amount', 'description', 'callback')


class CreatePaymentSerializer(serializers.ModelSerializer):
    cache_id = serializers.CharField(max_length=128)
    card_id = serializers.CharField(max_length=128)

    class Meta:
        model = Payment
        fields = ('cache_id', 'card_id')


class CompleteRefundPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('transaction_id',)
