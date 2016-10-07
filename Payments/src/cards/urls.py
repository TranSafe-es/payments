from django.conf.urls import url
from . import views

urlpatterns = [
    #  client side
    url(r'^create/$', views.InitAddView.as_view()),
    url(r'^update/(?P<user_id>.+)/$', views.InitUpdateView.as_view()),
    url(r'^delete/(?P<user_id>.+)/$', views.DeleteCardView.as_view({'get': 'retrieve'})),

    #  server side
    url(r'^add_card/(?P<cache_id>.+)/$', views.AddCardView.as_view({'get': 'retrieve',
                                                                   'post': 'create'})),

    url(r'^edit_card/(?P<cache_id>.+)/(?P<card_id>.+)/$', views.UpdateCard.as_view()),
    url(r'^edit_card/(?P<cache_id>.+)/$', views.UpdateCardView.as_view()),
    url(r'^get_card/(?P<card_id>.+)/$', views.CardsViewSet.as_view({'get': 'retrieve'})),


    url(r'^$', views.CardsViewSet.as_view({'get': 'list'})),

]
