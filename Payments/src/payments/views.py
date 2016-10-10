from django.shortcuts import render, redirect
from .models import Card
#from .serializers import CardSerializer, UpdateCardSerializer, DeleteCardSerializer, UserIDSerializer
from rest_framework import viewsets, status, mixins, views
import uuid
import datetime
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.http import HttpResponse


class InitTransactionView(views.APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        cache_id = str(uuid.uuid4().get_hex().upper()[0:6])
        serializer = UserIDSerializer(data=kwargs)

        #serializer = UserIDSerializer(data=request.data)
        if serializer.is_valid():
            #data = {"user_id": serializer.validated_data["user_id"], "url": request.META.get("HTTP_REFERER")}
            data = {"user_id1": kwargs["user_id1"], "user_id2": kwargs["user_id2"], "url": "http://www.google.pt"}

            cache.set(cache_id, data)
            for key in request.session.keys():
                del request.session[key]
            return redirect('/api/v1/cards/add_card/' + cache_id + "/")
        else:
            return HttpResponse({'status': 'Bad Request',
                                 'message': 'Unexpected error'},
                                status=status.HTTP_400_BAD_REQUEST)