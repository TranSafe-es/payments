from django.conf.urls import url
from . import views

urlpatterns = [
    #  client side
    url(r'^create/(?P<user_id1>.+)/(?P<user_id2>.+)/(?P<transaction_id>.+)/(?P<amount>.+)/(?P<description>.+)/$',
        views.InitPaymentView.as_view()),
    #  url(r'^update/(?P<user_id>.+)/$', views.InitUpdateView.as_view()),
    #  url(r'^delete/(?P<user_id>.+)/$', views.InitDeleteView.as_view()),
    #url(r'^create/$', views.InitPaymentView.as_view()),
    #url(r'^update/$', views.InitUpdateView.as_view()),
    #url(r'^delete/$', views.InitDeleteView.as_view()),

    #  server side
    url(r'^confirm_payment/(?P<cache_id>.+)/$', views.CreatePaymentView.as_view({'get': 'retrieve',
                                                                                 'post': 'create'})),

    #url(r'^edit_card/(?P<cache_id>.+)/(?P<card_id>.+)/$', views.UpdateCard.as_view()),
    #url(r'^edit_card/(?P<cache_id>.+)/$', views.UpdateCardView.as_view()),
    #url(r'^delete_card/(?P<cache_id>.+)/(?P<card_id>.+)/$', views.DeleteCard.as_view()),
    #url(r'^delete_card/(?P<cache_id>.+)/$', views.DeleteCardView.as_view()),

]
