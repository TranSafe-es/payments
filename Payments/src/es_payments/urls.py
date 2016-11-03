from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from cards.views import AddCardView
from payments.urls import urlpatterns as paymentsurls
from cards.urls import urlpatterns as cardsurls
from appManagement.urls import urlpatterns as appsurls
from django.views.decorators.cache import never_cache


urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

               # pages
               url(r'^api/v1/payments/', include(paymentsurls)),
               url(r'^api/v1/cards/', include(cardsurls)),
               url(r'^api/v1/apps/', include(appsurls)),
               url('^$', TemplateView.as_view(template_name='index.html'), name='index'),

               ]
