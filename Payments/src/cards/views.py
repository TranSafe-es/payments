from django.utils.cache import patch_cache_control
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Card
from .serializers import CardSerializer, UpdateCardSerializer, DeleteCardSerializer, MyCardsSerializer, \
    ListCardsSerializer, UserIDSerializer
from rest_framework import viewsets, status, mixins, views
import uuid
import datetime
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.utils.cache import add_never_cache_headers


class InitAddView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        #serializer = UserIDSerializer(data=kwargs)

        serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            data = {"user_id": serializer.validated_data["user_id"], "url": request.META.get("HTTP_REFERER")}
            #data = {"user_id": kwargs["user_id"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)

            return redirect('/api/v1/cards/add_card/' + cache_id + "/")
        else:
            response = Response({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)
            return redirect(request.META.get("HTTP_REFERER"), response)


class AddCardView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, views.APIView):
    def retrieve(self, request, *args, **kwargs):
        template = "add_Card.html"
        for key in request.session.keys():
            del request.session[key]

        request.session["cancel"] = cache.get(kwargs["cache_id"])["url"]
        return render(request, template)

    def create(self, request, **kwargs):
        serializer = CardSerializer(data=request.data)
        for key in request.session.keys():
            del request.session[key]
        request.session["cancel"] = cache.get(request.data["cache_id"])["url"]

        if serializer.is_valid():
            user_id = cache.get(serializer.validated_data["cache_id"])["user_id"]

            if Card.objects.filter(user_id=user_id, number=serializer.validated_data["number"],
                                   cvv2=serializer.validated_data["cvv2"]).count() is 1:

                request.session["error"] = "This card already exists"
                for data in request.data:
                        request.session[data] = str(request.data[data])
                template = "add_Card.html"
                return render(request, template)
            else:
                errors = False
                if not len(serializer.validated_data["number"]) == 16:
                    errors = True
                    request.session["number_error"] = "The card number needs 16 digits"
                if not len(serializer.validated_data["cvv2"]) == 3:
                    errors = True
                    request.session["cvv2_error"] = "The CVV value needs 3 digits"
                if serializer.validated_data["expire_month"] < 1 or serializer.validated_data["expire_month"] > 12:
                    errors = True
                    request.session["expire_month_error"] = "Month should be between 1 and 12"

                if errors:
                    for data in request.data:
                        request.session[data] = str(request.data[data])
                    template = "add_Card.html"
                    return render(request, template)

                now = datetime.datetime.now()

                if serializer.validated_data["expire_year"] < now.year:
                    if serializer.validated_data["expire_year"] == now.year and \
                       serializer.validated_data["expire_month"] < now.month:
                        request.session["date_error"] = "This expire date is not valid"
                        for data in request.data:
                            request.session[data] = str(request.data[data])
                        template = "add_Card.html"
                        return render(request, template)

                Card.objects.create(user_id=user_id,
                                    card_id=uuid.uuid4(),
                                    number=serializer.validated_data["number"],
                                    expire_month=serializer.validated_data["expire_month"],
                                    expire_year=serializer.validated_data["expire_year"],
                                    cvv2=serializer.validated_data["cvv2"],
                                    first_name=serializer.validated_data["first_name"],
                                    last_name=serializer.validated_data["last_name"])

                response = Response({'status': 'Associated',
                                     'message': 'The card has been associated successfully.'},
                                    status=status.HTTP_200_OK)
                return redirect(cache.get(serializer.validated_data["cache_id"])["url"], response)

        for error in serializer.errors:
            s = error + "_error"
            request.session[s] = str(serializer.errors[error][0])

        for data in request.data:
            request.session[data] = str(request.data[data])
        template = "add_Card.html"
        return render(request, template)


class UpdateCardView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):
        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        cache.set(cache_id, kwargs["user_id"])

        data = {'url': '192.168.33.10/update_card/' + cache_id}
        return Response(data=data,
                        status=status.HTTP_302_FOUND)


class DeleteCardView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):
        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        cache.set(cache_id, kwargs["user_id"])

        data = {'url': '192.168.33.10/delete_card/' + cache_id}
        return Response(data=data,
                        status=status.HTTP_302_FOUND)


class CardsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):

        if Card.objects.filter(card_id=kwargs["card_id"]).count() == 0:
            return Response({'status': 'Nonexistent card',
                             'message': 'The card doesn\'t exists'},
                            status=status.HTTP_404_NOT_FOUND)
        elif Card.objects.filter(card_id=kwargs["card_id"]).count() == 1:
            c = Card.objects.get(card_id=kwargs["card_id"])

            card = {'number': "************" + c.number[-4:], 'expire_month': c.expire_month,
                    'expire_year': c.expire_year}

            card_serializer = MyCardsSerializer(card)

            return Response(card_serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Bad Request',
                             'message': 'Unexpected error'},
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serializer = ListCardsSerializer(data=request.query_params)

        if serializer.is_valid():
            user_id = cache.get(serializer.validated_data["cache_id"])

            if Card.objects.filter(user_id=user_id).count() != 0:
                cards = []
                for c in Card.objects.all():
                    if c.user_id == user_id:
                        card_data = {'card_id': c.card_id, 'number': "************" + c.number[-4:],
                                     'expire_month': c.expire_month, 'expire_year': c.expire_year}
                        cards.append(card_data)
                card_serializer = MyCardsSerializer(cards, many=True)

                return Response(card_serializer.data,
                                status=status.HTTP_200_OK)

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        serializer = UpdateCardSerializer(data=request.data)
        for f in serializer.fields:
            if f != "cache_id":
                serializer.fields[f].required = False
        if serializer.is_valid():
            user_id = cache.get(serializer.validated_data["cache_id"])

            now = datetime.datetime.now()

            if Card.objects.filter(user_id=user_id,
                                   card_id=kwargs["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                c = Card.objects.get(user_id=user_id,
                                     card_id=kwargs["card_id"])

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

        if serializer.is_valid():
            user_id = cache.get(serializer.validated_data["cache_id"])

            if Card.objects.filter(user_id=user_id,
                                   card_id=kwargs["card_id"]).count() is 0:
                return Response({'status': 'Doesn\'t have associated',
                                 'message': 'The user doesn\'t have this card associated to him.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            else:
                c = Card.objects.get(user_id=user_id,
                                     card_id=kwargs["card_id"])
                c.delete()

                return Response({'status': 'Deleted',
                                 'message': 'The card has been deleted successfully.'},
                                status=status.HTTP_200_OK)
        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST
                        )