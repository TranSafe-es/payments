from rest_framework import serializers
from cards.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('user_id', 'card_id', 'number', 'expire_month', 'expire_year', 'cvv2', 'first_name', 'last_name',
                  'total')
        read_only_fields = ('card_id', 'total')


class UpdateCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('user_id', 'card_id', 'number', 'expire_month', 'expire_year', 'cvv2', 'first_name', 'last_name',
                  'total')
        read_only_fields = ('card_id', )


class DeleteCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('user_id', 'card_id')
        read_only_fields = ('card_id', )



class ListCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('user_id',)

