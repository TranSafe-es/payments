from django.conf.urls import url
from . import views

urlpatterns = [
    #  client side
    #  url(r'^create/(?P<user_id1>.+)/(?P<user_id2>.+)/(?P<transaction_id>.+)/(?P<amount>.+)/(?P<description>.+)/$',
    #    views.InitPaymentView.as_view()),
    #  url(r'^complete/(?P<transaction_id>.+)/$', views.CompletePaymentView.as_view()),
    #  url(r'^refund/(?P<transaction_id>.+)/$', views.RefundPaymentView.as_view()),
    url(r'^create/$', views.InitPaymentView.as_view()),
    url(r'^complete/$', views.CompletePaymentView.as_view()),
    url(r'^refund/$', views.RefundPaymentView.as_view()),

    #  server side
    url(r'^confirm_payment/(?P<cache_id>.+)/$', views.CreatePaymentView.as_view({'get': 'retrieve',
                                                                                 'post': 'create'})),


]
