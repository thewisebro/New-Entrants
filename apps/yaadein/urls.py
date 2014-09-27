
from django.conf.urls import url

from yaadein import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    ]

