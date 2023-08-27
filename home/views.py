from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import requests
from rest_framework.exceptions import NotFound, APIException
from rest_framework import serializers
from .models import URL
from .serializers import URLSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
   
    #permission_classes = [IsAuthenticated, ]
    
    #Shortens the url
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(responses={201: "Successfully added!"})
    def shorten(self, request):
        ip_address = self.request.META.get('REMOTE_ADDR')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = serializer.validated_data.get('short_url')
        # created_user= request.user

        try:
            #checks if custom url is provided.If not generates a new short_url
            if short_url:
                instance = URL.objects.filter(short_url=short_url).first()
                try:
                    if instance:
                        raise serializers.ValidationError(
                            "URL with the given short URL already exists.")
                except Exception as e:
                    return response("Url with this short url already exists!.", status=status.HTTP_406_NOT_ACCEPTABLE)

                if not instance:
                    instance = URL()
                    # instance.created_by=created_user
                    instance.original_url = serializer.validated_data['original_url']
                    instance.short_url = serializer.validated_data['short_url']
                    instance.click_count = 0
                    instance.referral_sources.append(
                        request.META.get('HTTP_REFERER'))
                    response = requests.get(
                        f'http://ipinfo.io/{ip_address}/json')
                    location_data = response.json()
                    instance.locations.append(location_data)
                    instance.save(ip_address=ip_address)
                    return Response({"message": "Successfully added!", "short_url": instance.short_url}, status=status.HTTP_201_CREATED)

        # instance = URL(original_url=serializer.validated_data['original_url'],created_by=created_user)
            instance = URL(
                original_url=serializer.validated_data['original_url'])
            instance.save(ip_address=ip_address)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Successfully added!", "short_url": instance.short_url}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response("error occured while adding", status=status.HTTP_400_BAD_REQUEST)

    #Redirects to the original url
    @action(detail=True, methods=['get'])
    @swagger_auto_schema(responses={201: "Successfully added!"})
    def redirect(self, request, short_url=None):
        #checks if the given short_url is found
        if not short_url:
            return Response({"error": "Parameter 'short_url' is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = URL.objects.get(short_url=short_url)
        except URL.DoesNotExist:
            raise NotFound("Short URL not found.")
        try:
            instance.click_count += 1
            if instance.click_count > 10:
                instance.delete()
                raise NotFound(
                    "Short URL is exhausted due to excessive clicks.")
            referral_source = request.META.get('HTTP_REFERER')
            if referral_source:
                instance.referral_sources.append(referral_source)
            ip_address = request.META.get('REMOTE_ADDR')
            response = requests.get(f'http://ipinfo.io/{ip_address}/json')
            location_data = response.json()
            instance.locations.append(location_data)
            instance.save()
            return redirect(instance.original_url)
        except Exception as e:
            raise APIException({" Error:", "e", e})
            
    #analytics(provide the click count lacation and referral sources)
    @action(detail=True, methods=['get'])
    @swagger_auto_schema(responses={201: "Successfully added!"})
    def stats(self, request, short_url=None):
        if not short_url:
            return Response({"error": "Parameter 'short_url' is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = URL.objects.get(short_url=short_url)
        except URL.DoesNotExist:
            raise NotFound("Short URL not found.")
        response_data = {
            "original_url": instance.original_url,
            "click_count": instance.click_count,
            "referral_sources": instance.referral_sources
        }
        return Response(response_data, status=status.HTTP_200_OK)
