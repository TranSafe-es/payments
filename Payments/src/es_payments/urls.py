from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
#from payments.urls import urlpatterns as dataurls
from cards.urls import urlpatterns as cardsurls

urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

               # pages
               #url(r'^api/v1/payments/', include(dataurls)),
               url(r'^api/v1/cards/', include(cardsurls)),

               url('^.*$', TemplateView.as_view(template_name='index.html'), name='index')
               ]

