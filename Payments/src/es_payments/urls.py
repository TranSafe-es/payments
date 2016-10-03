from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from cards.views import AddCardView
#from payments.urls import urlpatterns as dataurls
from cards.urls import urlpatterns as cardsurls


urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

               # pages
               #url(r'^api/v1/payments/', include(dataurls)),
               url(r'^api/v1/cards/', include(cardsurls)),
               url(r'^add_card/(?P<cache_id>.+)$', TemplateView.as_view(template_name='add_Card.html'), name='addCard'),
               url('^$', TemplateView.as_view(template_name='index.html'), name='index'),

               ]

