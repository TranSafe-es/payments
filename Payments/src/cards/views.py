import status as status
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer, UpdateCardSerializer, DeleteCardSerializer, ListCardSerializer, \
    MyCardsSerializer
from rest_framework import viewsets, status, mixins, views
from django.db import transaction
from django.db import IntegrityError
import uuid
import datetime


class CardsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        serializer = ListCardSerializer(data=request.query_params)

        if serializer.is_valid():
            cards = []
            for c in Card.objects.all():
                if c.user_id == serializer.validated_data["user_id"]:
                    card_data = {'number': "************" + c.number[-4:], 'expire_month': c.expire_month,
                                 'expire_year': c.expire_year}
                    cards.append(card_data)
            card_serializer = MyCardsSerializer(cards, many=True)

            return Response(card_serializer.data,
                            status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    def create(self, request, **kwargs):
        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():
            if Card.objects.filter(user_id=serializer.validated_data["user_id"], number=serializer.validated_data["number"],
                                   cvv2=serializer.validated_data["cvv2"]).count() is 1:
                return Response({'status': 'Already Exists',
                                 'message': 'The card already exists.'},
                                status=status.HTTP_401_UNAUTHORIZED
                                )
            else:
                if not len(serializer.validated_data["number"]) == 16 or \
                                not len(serializer.validated_data["cvv2"]) == 3 or \
                                serializer.validated_data["expire_month"] < 1 or \
                                serializer.validated_data["expire_month"] > 12:

                        now = datetime.datetime.now()

                        if serializer.validated_data["expire_year"] < now.year:
                            if serializer.validated_data["expire_year"] == now.year and \
                               serializer.validated_data["expire_month"] < now.month:
                                return Response({'status': 'Expiration Date',
                                                 'message': 'The card expired.'},
                                                status=status.HTTP_403_FORBIDDEN)
                        Card.objects.create(user_id=serializer.validated_data["user_id"],
                                            card_id=uuid.uuid4(),
                                            number=serializer.validated_data["number"],
                                            expire_month=serializer.validated_data["expire_month"],
                                            expire_year=serializer.validated_data["expire_year"],
                                            cvv2=serializer.validated_data["cvv2"],
                                            first_name=serializer.validated_data["first_name"],
                                            last_name=serializer.validated_data["last_name"])

                return Response({'status': 'Associated',
                                 'message': 'The card has been associated successfully.'},
                                status=status.HTTP_200_OK
                                )

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error',
                         'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    def update(self, request, **kwargs):
        serializer = UpdateCardSerializer(data=request.data)
        for f in serializer.fields:
            if f != "card_id" and f != "user_id":
                serializer.fields[f].required = False
            elif f == "card_id":
                serializer.fields[f].required = True
        if serializer.is_valid():
            now = datetime.datetime.now()

            if Card.objects.filter(user_id=serializer.validated_data["user_id"],
                                   card_id=request.data["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                c = Card.objects.get(user_id=serializer.validated_data["user_id"],
                                     card_id=request.data["card_id"])

                try:
                    if len(serializer.validated_data["number"]) == 16:
                        c.number = serializer.validated_data["number"]
                    else:
                        return Response({'status': 'Number error',
                                        'message': 'The card number should contain 16 digits'},
                                        status=status.HTTP_403_FORBIDDEN)
                except KeyError:
                    pass
                try:
                    if len(serializer.validated_data["cvv2"]) == 3:
                        c.cvv2 = serializer.validated_data["cvv2"]
                    else:
                        return Response({'status': 'CVV2 error',
                                        'message': 'The card cvv2 should contain 3 digits'},
                                        status=status.HTTP_403_FORBIDDEN)
                except KeyError:
                    pass
                try:
                    c.first_name = serializer.validated_data["first_name"]
                except KeyError:
                    pass
                try:
                    c.last_name = serializer.validated_data["last_name"]
                except KeyError:
                    pass
                same_year_now = False
                try:
                    if serializer.validated_data["expire_year"] >= now.year:
                        c.expire_year = serializer.validated_data["expire_year"]
                        if serializer.validated_data["expire_year"] == now.year:
                            same_year_now = True
                    else:
                        return Response({'status': 'Year error',
                                        'message': 'The card expire year should be valid'},
                                        status=status.HTTP_403_FORBIDDEN)
                except KeyError:
                    pass
                try:
                    if 1 <= serializer.validated_data["expire_month"] <= 12:
                        if same_year_now is True and serializer.validated_data["expire_month"] < now.month:
                            return Response({'status': 'Month error',
                                             'message': 'The card expire month should be valid'},
                                            status=status.HTTP_403_FORBIDDEN)
                        else:
                            c.expire_month = serializer.validated_data["expire_month"]
                except KeyError:
                    pass

                c.save()

                return Response({'status': 'Updated',
                                 'message': 'The card has been updated successfully.'},
                                status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error',
                         'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    def destroy(self, request, *args, **kwargs):
        serializer = DeleteCardSerializer(data=request.data)
        for f in serializer.fields:
            if f == "card_id":
                serializer.fields[f].required = True
        if serializer.is_valid():
            if Card.objects.filter(user_id=serializer.validated_data["user_id"],
                                   card_id=request.data["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            else:
                c = Card.objects.get(user_id=serializer.validated_data["user_id"],
                                     card_id=request.data["card_id"])
                c.delete()

                return Response({'status': 'Deleted',
                                 'message': 'The card has been deleted successfully.'},
                                status=status.HTTP_200_OK)
        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST
                        )