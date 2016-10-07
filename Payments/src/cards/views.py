from django.shortcuts import render, redirect
from .models import Card
from .serializers import CardSerializer, UpdateCardSerializer, DeleteCardSerializer, UserIDSerializer
from rest_framework import viewsets, status, mixins, views
import uuid
import datetime
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.http import HttpResponse


class InitAddView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        #  serializer = UserIDSerializer(data=kwargs)

        serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            data = {"user_id": serializer.validated_data["user_id"], "url": request.META.get("HTTP_REFERER")}
            #  data = {"user_id": kwargs["user_id"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)
            for key in request.session.keys():
                del request.session[key]
            return redirect('/api/v1/cards/add_card/' + cache_id + "/")
        else:
            return HttpResponse({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)


class InitUpdateView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        #  serializer = UserIDSerializer(data=kwargs)

        serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            data = {"user_id": serializer.validated_data["user_id"], "url": request.META.get("HTTP_REFERER")}
            #  data = {"user_id": kwargs["user_id"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)
            for key in request.session.keys():
                del request.session[key]
            return redirect('/api/v1/cards/edit_card/' + cache_id + "/")
        else:
            return HttpResponse({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)


class InitDeleteView(views.APIView):
    @staticmethod
    def post(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        #  serializer = UserIDSerializer(data=kwargs)

        serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            data = {"user_id": serializer.validated_data["user_id"], "url": request.META.get("HTTP_REFERER")}
            #  data = {"user_id": kwargs["user_id"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)
            for key in request.session.keys():
                del request.session[key]

            return redirect('/api/v1/cards/delete_card/' + cache_id + "/")
        else:
            return HttpResponse({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)


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
        if cache.get(request.data["cache_id"]) is not None:
            request.session["cancel"] = cache.get(request.data["cache_id"])["url"]
            user_id = cache.get(request.data["cache_id"])["user_id"]
            if serializer.is_valid():
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

                    return redirect(cache.get(serializer.validated_data["cache_id"])["url"])

            for error in serializer.errors:
                s = error + "_error"
                request.session[s] = str(serializer.errors[error][0])

        for data in request.data:
            request.session[data] = str(request.data[data])
        template = "add_Card.html"
        return render(request, template)


class UpdateCardView(views.APIView):
    @staticmethod
    @never_cache
    def get(request, *args, **kwargs):
        template = "update_Card_choose.html"
        for key in request.session.keys():
            del request.session[key]

        user_id = cache.get(kwargs["cache_id"])["user_id"]

        cards = []
        for c in Card.objects.all():
            if c.user_id == user_id:
                card_data = {'card_id': c.card_id, 'number': "************" + c.number[-4:]}
                cards.append(card_data)

        request.session["card"] = []
        for c in cards:
            request.session["card"].append({'card_id': c["card_id"], 'number': c["number"]})

        request.session["cancel"] = cache.get(kwargs["cache_id"])["url"]
        return render(request, template)


class UpdateCard(views.APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        if request.POST["choose"] == "True":
            template = "update_Card.html"
            for key in request.session.keys():
                del request.session[key]

            c = Card.objects.get(card_id=kwargs["card_id"])

            request.session["first_name"] = c.first_name
            request.session["last_name"] = c.last_name
            request.session["expire_month"] = c.expire_month
            request.session["expire_year"] = c.expire_year
            request.session["cancel"] = request.META.get("HTTP_REFERER")
            return render(request, template)

        else:
            serializer = UpdateCardSerializer(data=request.data)
            for f in serializer.fields:
                if f != "cache_id":
                    serializer.fields[f].required = False
            for key in request.session.keys():
                if key != "cancel":
                    del request.session[key]

            if cache.get(request.data["cache_id"]) is not None:
                if serializer.is_valid():
                    user_id = cache.get(serializer.validated_data["cache_id"])["user_id"]

                    now = datetime.datetime.now()

                    errors = False
                    if Card.objects.filter(user_id=user_id,
                                           card_id=kwargs["card_id"]).count() is 0:

                        request.session["error"] = "This card doesn't exists"
                        template = "update_Card.html"
                        return render(request, template)
                    else:
                        c = Card.objects.get(user_id=user_id,
                                             card_id=kwargs["card_id"])

                        try:
                            if len(serializer.validated_data["number"]) == 16:
                                c.number = serializer.validated_data["number"]
                            else:
                                errors = True
                                request.session["number_error"] = "The card number should contain 16 digits"
                        except KeyError:
                            pass
                        try:
                            if len(serializer.validated_data["cvv2"]) == 3:
                                c.cvv2 = serializer.validated_data["cvv2"]
                            else:
                                errors = True
                                request.session["cvv2_error"] = "The card cvv2 should contain 3 digits"
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
                                errors = True
                                request.session["expire_year_error"] = "The card expire year should be valid"
                        except KeyError:
                            pass
                        try:
                            if 1 <= serializer.validated_data["expire_month"] <= 12:
                                if same_year_now is True and serializer.validated_data["expire_month"] < now.month:
                                    errors = True
                                    request.session["expire_month_error"] = "The card expire month should be valid"
                                else:
                                    c.expire_month = serializer.validated_data["expire_month"]
                            else:
                                errors = True
                                request.session["expire_month_error"] = "The card expire month should be valid"
                        except KeyError:
                            pass

                        if errors:
                            for data in request.data:
                                request.session[data] = str(request.data[data])
                            template = "update_Card.html"
                            return render(request, template)
                        else:
                            c.save()
                            for key in request.session.keys():
                                del request.session[key]

                            return redirect('/api/v1/cards/edit_card/' + serializer.validated_data["cache_id"] + "/")

                for error in serializer.errors:
                    s = error + "_error"
                    request.session[s] = str(serializer.errors[error][0])

            for data in request.data:
                request.session[data] = str(request.data[data])
            template = "update_Card.html"
            return render(request, template)


class DeleteCardView(views.APIView):
    @staticmethod
    @never_cache
    def get(request, *args, **kwargs):
        template = "delete_Card.html"
        for key in request.session.keys():
            if key != "delete_error":
                del request.session[key]

        user_id = cache.get(kwargs["cache_id"])["user_id"]

        cards = []
        for c in Card.objects.all():
            if c.user_id == user_id:
                card_data = {'card_id': c.card_id, 'number': "************" + c.number[-4:]}
                cards.append(card_data)

        request.session["card"] = []
        for c in cards:
            request.session["card"].append({'card_id': c["card_id"], 'number': c["number"]})

        request.session["cancel"] = cache.get(kwargs["cache_id"])["url"]
        return render(request, template)


class DeleteCard(views.APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = DeleteCardSerializer(data=request.data)
        if cache.get(request.data["cache_id"]) is not None:
            request.session["cancel"] = cache.get(kwargs["cache_id"])["url"]

            if serializer.is_valid():
                user_id = cache.get(serializer.validated_data["cache_id"])["user_id"]

                if Card.objects.filter(user_id=user_id,
                                       card_id=kwargs["card_id"]).count() is 0:

                    request.session["delete_error"] = "The user doesn\'t have this card associated to him."
                    return redirect('/api/v1/cards/delete_card/' + serializer.validated_data["cache_id"] + "/")
                else:
                    c = Card.objects.get(user_id=user_id,
                                         card_id=kwargs["card_id"])
                    c.delete()
                    for key in request.session.keys():
                        del request.session[key]

                    return redirect('/api/v1/cards/delete_card/' + serializer.validated_data["cache_id"] + "/")

            request.session["delete_error"] = "Unexpected Error."
            template = "delete_Card.html"
            return render(request, template)
