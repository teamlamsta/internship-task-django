from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions as pe
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from home.serializers import UrlSerializer, UrlAnalyticsSerializer
from home.models import UrlShortner

class ShortnerCreateView(CreateAPIView):
    serializer_class = UrlSerializer
    permission_classes = [AllowAny]

    def create(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data

        try:
            url_short = UrlShortner.objects.create(incoming_url= data.get('incoming_url'), outgoing_url = data.get('outgoing_url'))
            url_short.save()
            return Response({"message": "Successfully Created Short URL"},201)
        except Exception as e:
            return Response({"detail":"Error Occured"},400)

shortner_create_view = ShortnerCreateView.as_view()

class ShortnerRedirectView(RetrieveAPIView):
    queryset = UrlShortner.objects.filter(is_active=True)
    serializer_class = UrlSerializer
    lookup_field = "slug"
    permission_classes =[AllowAny]

    def get_queryset(self):
        return UrlShortner.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(incoming_url=self.kwargs[self.lookup_field]).first()
        if queryset:
            serializer = self.serializer_class(queryset, many=False)
            queryset.click_through_counter = queryset.click_through_counter + 1
            queryset.save()
            return HttpResponseRedirect(redirect_to=serializer.data["outgoing_url"])
        return Response({"detail": "Not Found"}, 404)
    
shortner_redirect_view = ShortnerRedirectView.as_view()

class ShortnerAnalyticsView(RetrieveAPIView):
    queryset = UrlShortner.objects.filter(is_active=True)
    serializer_class = UrlAnalyticsSerializer
    lookup_field = "slug"
    permission_classes =[AllowAny]

    def get_queryset(self):
        return UrlShortner.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(incoming_url=self.kwargs[self.lookup_field]).first()
        if queryset:
            serializer = self.serializer_class(queryset, many=False)
            return Response(serializer.data,200)
        return Response({"detail": "Not Found"}, 404)
    
shortner_analytics_view = ShortnerAnalyticsView.as_view()