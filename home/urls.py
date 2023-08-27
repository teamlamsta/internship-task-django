from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import URLViewSet
router = DefaultRouter()
router.register(r'urls', URLViewSet, basename='url')


urlpatterns = [
    path('', include(router.urls)),
    path('redirect/<str:short_url>/',
         URLViewSet.as_view({'get': 'redirect'}), name='url-redirect'),
    path('analytics/<str:short_url>/',
         URLViewSet.as_view({'get': 'stats'}), name='url-analytics'),
]
