import status as status
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer, UpdateCardSerializer, DeleteCardSerializer, ListCardSerializer
from rest_framework import viewsets, status, mixins, views
from django.db import transaction
from django.db import IntegrityError
import uuid


class CardsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        serializer = ListCardSerializer(data=request.query_params)

        if serializer.is_valid():
            for c in Card.objects.all():
                a = c.number
                b = c.cvv2
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
                         'message': 'Unexpected error'},
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
            if Card.objects.filter(user_id=serializer.validated_data["user_id"],
                                   card_id=serializer.validated_data["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                c = Card.objects.get(user_id=serializer.validated_data["user_id"],
                                     card_id=serializer.validated_data["card_id"])

                try:
                    c.number = serializer.validated_data["number"]
                except KeyError:
                    pass
                try:
                    c.cvv2 = serializer.validated_data["cvv2"]
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
                try:
                    c.expire_month = serializer.validated_data["expire_month"]
                except KeyError:
                    pass
                try:
                    c.expire_year = serializer.validated_data["expire_year"]
                except KeyError:
                    pass
                c.save()

                return Response({'status': 'Updated',
                                 'message': 'The card has been updated successfully.'},
                                status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    def destroy(self, request, *args, **kwargs):
        serializer = DeleteCardSerializer(data=request.data)

        if serializer.is_valid():
            if Card.objects.filter(user_id=serializer.validated_data["user_id"],
                                   card_id=serializer.validated_data["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            else:
                c = Card.objects.get(user_id=serializer.validated_data["user_id"],
                                     card_id=serializer.validated_data["card_id"])
                c.delete()

                return Response({'status': 'Deleted',
                                 'message': 'The card has been deleted successfully.'},
                                status=status.HTTP_200_OK)
        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST
                        )