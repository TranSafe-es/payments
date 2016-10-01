from django.conf.urls import url
from . import views

urlpatterns = [
               url(r'^$', views.CardsViewSet.as_view({'post': 'create',
                                                      'put': 'update',
                                                      'delete': 'destroy',
                                                      'get': 'list'})),
]