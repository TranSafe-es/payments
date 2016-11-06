import datetime
import socket
import uuid
from django.shortcuts import render, redirect
from .models import App
from rest_framework import viewsets, status, mixins, views
from django.views.decorators.cache import never_cache
from rest_framework.response import Response



class CreateAppView(views.APIView):
    @staticmethod
    @never_cache
    def post(request, *args, **kwargs):
        if request.data["name"] is None:
            a = App.objects.create()
        else:
            a = App.objects.create(name=request.data["name"])

        return Response({'token_id': a.token_id},
                        status=status.HTTP_200_OK)

class ShowAppTemplate(views.APIView):

    @staticmethod
    @never_cache
    def get(request, *args, **kwargs):
        return render(request, "index.html")
