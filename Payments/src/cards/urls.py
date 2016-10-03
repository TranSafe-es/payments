from django.conf.urls import url
from . import views

urlpatterns = [
    #  return url's
    url(r'^create/(?P<user_id>.+)/$', views.AddCardView.as_view({'get': 'retrieve'})),
    url(r'^update/(?P<user_id>.+)/$', views.UpdateCardView.as_view({'get': 'retrieve'})),
    url(r'^delete/(?P<user_id>.+)/$', views.DeleteCardView.as_view({'get': 'retrieve'})),

    #  server side
    url(r'^get_card/(?P<card_id>.+)/$', views.CardsViewSet.as_view({'get': 'retrieve'})),

    url(r'^edit_card/(?P<card_id>.+)/$', views.CardsViewSet.as_view({'put': 'update',
                                                                     'delete': 'destroy'})),
    url(r'^$', views.CardsViewSet.as_view({'post': 'create',
                                           'get': 'list'})),

]
