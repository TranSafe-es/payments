from django.shortcuts import render, redirect
from .models import Card
from .serializers import PaymentSerializer
from rest_framework import viewsets, status, mixins, views
import uuid
import datetime
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.http import HttpResponse


class InitPaymentView(views.APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        serializer = PaymentSerializer(data=kwargs)

        #serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            #  data = {"user_id1": serializer.validated_data["user_id1"],
            #        "user_id2": serializer.validated_data["user_id2"],
            #        "transaction_id": serializer.validated_data["transaction_id"],
            #        "amount": serializer.validated_data["amount"],
            #        "description": serializer.validated_data["description"], "url": "http://www.google.pt"}
            data = {"user_id": kwargs["user_id1"], "user_id2": kwargs["user_id2"],
                    "transaction_id": kwargs["transaction_id"], "amount": kwargs["amount"],
                    "description": kwargs["description"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)
            for key in request.session.keys():
                del request.session[key]

            return redirect('/api/v1/payments/confirm_payment/' + cache_id + "/")

        else:
            return HttpResponse({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)


class CreatePaymentView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    @never_cache
    def retrieve(self, request, *args, **kwargs):
        template = "payment.html"
        for key in request.session.keys():
                del request.session[key]
        if cache.get(kwargs["cache_id"]) is not None:
            c = cache.get(kwargs["cache_id"])
            user_id = c["user_id"]
            request.session["description"] = c["description"]
            request.session["amount"] = c["amount"]
            request.session["cancel"] = c["url"]
            if Card.objects.filter(user_id=user_id).count() == 0:
                request.session["error"] = "Please associate a card to your account"
            else:
                cards = []
                for c in Card.objects.all():
                    if c.user_id == user_id:
                        card_data = {'card_id': c.card_id, 'number': "************" + c.number[-4:]}
                        cards.append(card_data)

                request.session["card"] = []
                for c in cards:
                    request.session["card"].append({'card_id': c["card_id"], 'number': c["number"]})

            return render(request, template)

        return HttpResponse({'status': 'Bad Request',
                             'message': 'Unexpected error'},
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        for key in request.session.keys():
            del request.session[key]
        if cache.get(request.data["cache_id"]) is not None:
            request.session["cancel"] = cache.get(request.data["cache_id"])["url"]
            user_id = cache.get(request.data["cache_id"])["user_id"]

            for error in serializer.errors:
                s = error + "_error"
                request.session[s] = str(serializer.errors[error][0])

        for data in request.data:
            request.session[data] = str(request.data[data])
        template = "payment.html"
        return render(request, template)