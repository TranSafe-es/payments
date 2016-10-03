from rest_framework import serializers
from cards.models import Card


class CardSerializer(serializers.ModelSerializer):
    cache_id = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = Card
        fields = ('cache_id', 'card_id', 'number', 'expire_month', 'expire_year', 'cvv2', 'first_name', 'last_name',
                  'total')
        read_only_fields = ('card_id', 'total')


class UpdateCardSerializer(serializers.ModelSerializer):
    cache_id = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = Card
        fields = ('cache_id', 'number', 'expire_month', 'expire_year', 'cvv2', 'first_name', 'last_name',
                  'total')
        read_only_fields = ('card_id', )


class DeleteCardSerializer(serializers.ModelSerializer):
    cache_id = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = Card
        fields = ('cache_id',)
        read_only_fields = ('card_id', )


class MyCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('number', 'expire_month', 'expire_year')


class ListCardsSerializer(serializers.ModelSerializer):
    cache_id = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = Card
        fields = ('cache_id',)
