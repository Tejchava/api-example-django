from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^main/$', views.login, name="login"),
    url(r'^greet/$', views.greet, name="greet"),
]