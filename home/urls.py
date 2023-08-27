from django.urls import path, include
from rest_framework import routers
from home.views import shortner_create_view, shortner_redirect_view, shortner_analytics_view

urlpatterns = [
    path('create/',shortner_create_view,name='create-shorturl'),
    path('<slug:slug>/',shortner_redirect_view,name='url-redirect'),
    path('<slug:slug>/analytics/',shortner_analytics_view,name='analytics'),
]

