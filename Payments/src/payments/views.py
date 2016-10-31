from django.shortcuts import render, redirect
from .models import Card, Payment
from .serializers import PaymentSerializer, CreatePaymentSerializer, CompleteRefundPaymentSerializer
from rest_framework import viewsets, status, mixins, views
import uuid
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from decimal import Decimal
from django.views.decorators.clickjacking import xframe_options_exempt


class InitPaymentView(views.APIView):

    @staticmethod
    @xframe_options_exempt
    def post(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        #  serializer = PaymentSerializer(data=kwargs)

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = {"user_id1": serializer.validated_data["user_id1"],
                    "user_id2": serializer.validated_data["user_id2"],
                    "transaction_id": serializer.validated_data["transaction_id"],
                    "amount": serializer.validated_data["amount"],
                    "description": serializer.validated_data["description"], "url": request.META.get("HTTP_REFERER"),
                    "callback": serializer.validated_data["callback"]}
            #  data = {"user_id": kwargs["user_id1"], "user_id2": kwargs["user_id2"],
            #       "transaction_id": kwargs["transaction_id"], "amount": kwargs["amount"],
            #       "description": kwargs["description"], "url": "http://www.google.pt"}

            if Card.objects.filter(user_id=serializer.validated_data["user_id2"]).count() > 0:
                cache.set(cache_id, data)

                for key in request.session.keys():
                    del request.session[key]

                return redirect('/api/v1/payments/confirm_payment/' + cache_id + "/")

            else:
                request.session["error_init"] = True
                return Response({'status': 'Without Cards',
                                 'message': 'The user doesn\'t have an associated card to receive the money'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'Bad Request',
                             'message': 'Unexpected error'},
                            status=status.HTTP_400_BAD_REQUEST)


class CreatePaymentView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    @xframe_options_exempt
    @never_cache
    def retrieve(self, request, *args, **kwargs):
        template = "payment.html"
        for key in request.session.keys():
            del request.session[key]
        if cache.get(kwargs["cache_id"]) is not None:
            c = cache.get(kwargs["cache_id"])
            user_id = c["user_id1"]
            request.session["description"] = c["description"]
            request.session["amount"] = str(c["amount"])
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

        return Response({'status': 'Bad Request',
                         'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST)

    @xframe_options_exempt
    @never_cache
    def create(self, request, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data)
        for key in request.session.keys():
            del request.session[key]
        if serializer.is_valid():
            if cache.get(serializer.validated_data["cache_id"]) is not None:
                c = cache.get(serializer.validated_data["cache_id"])
                user_id = c["user_id1"]
                user_id2 = c["user_id2"]
                amount = c["amount"]
                confirm = c["callback"]
                transaction_id = c["transaction_id"]
                description = c["description"]
                url = c["url"]
                request.session["cancel"] = url
                request.session["amount"] = str(c["amount"])
                request.session["description"] = description
                cards = []
                for c in Card.objects.all():
                    if c.user_id == user_id:
                        card_data = {'card_id': c.card_id, 'number': "************" + c.number[-4:]}
                        cards.append(card_data)

                request.session["card"] = []
                for c in cards:
                    request.session["card"].append({'card_id': c["card_id"], 'number': c["number"]})

                if Payment.objects.filter(transaction_id=transaction_id).count() < 1:
                    if Card.objects.filter(user_id=user_id, card_id=serializer.validated_data["card_id"]).count() > 0:
                        c1 = Card.objects.get(card_id=serializer.validated_data["card_id"])
                        if c1.total < Decimal(amount):
                            request.session["error_confirm"] = "This card doesn\'t have money to confirm the payment"
                            template = "payment.html"
                            return render(request, template)
                        c1.total = c1.total - Decimal(amount)
                        c1.save()
                        c2 = Card.objects.get(user_id=user_id2, defined=True)
                        Payment.objects.create(user_id1=user_id, user_id2=user_id2, card_1=c1, card_2=c2,
                                               amount=Decimal(amount), description=description,
                                               transaction_id=transaction_id)

                        return redirect(confirm)
                else:
                    request.session["error_confirm"] = "This transaction already exists"
                    template = "payment.html"
                    return render(request, template)

        request.session["error_confirm"] = "It was impossible to confirm this payment"
        template = "payment.html"
        return render(request, template)


class CompletePaymentView(views.APIView):

    @staticmethod
    @xframe_options_exempt
    def post(request, *args, **kwargs):
        serializer = CompleteRefundPaymentSerializer(data=request.data)

        if serializer.is_valid():
            if Payment.objects.filter(transaction_id=serializer.validated_data["transaction_id"],
                                      state="Pending").count() == 1:
                p = Payment.objects.get(transaction_id=serializer.validated_data["transaction_id"])
                c = p.card_2
                c.total = c.total + p.amount
                p.state = "Completed"
                p.save()
                c.save()

                return Response({'status': 'Payment Completed',
                                 'message': 'The payment has been completed successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Complete Payment Error',
                                 'message': 'This transaction can\'t be completed'},
                                status=status.HTTP_401_UNAUTHORIZED)

        return Response({'status': 'Bad Request',
                        'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST)


class RefundPaymentView(views.APIView):

    @staticmethod
    @xframe_options_exempt
    def post(request, *args, **kwargs):
        serializer = CompleteRefundPaymentSerializer(data=request.data)

        if serializer.is_valid():
            if Payment.objects.filter(transaction_id=serializer.validated_data["transaction_id"], state="Pending").count() == 1:
                p = Payment.objects.get(transaction_id=serializer.validated_data["transaction_id"])
                c = p.card_1
                c.total = c.total + p.amount
                p.state = "Refunded"
                p.save()
                c.save()

                return Response({'status': 'Payment Refunded',
                                 'message': 'The payment has been refunded successfully'},
                                status=status.HTTP_200_OK)

            else:
                return Response({'status': 'Refund Error',
                                 'message': 'This transaction can\'t be refunded'},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status': 'Bad Request',
                        'message': 'Unexpected error'},
                        status=status.HTTP_400_BAD_REQUEST)
