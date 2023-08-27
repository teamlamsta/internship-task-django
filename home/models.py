from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework import status
from django.contrib.auth import get_user_model
import random
import string
import requests
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class URL(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    original_url = models.URLField()
    short_url = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    click_count = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(11), MinValueValidator(0)])
    locations = models.JSONField(default=list)
    referral_sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, ip_address=None, *args, **kwargs):
        try:
            if not self.short_url:
                existing_url = URL.objects.filter(
                    original_url=self.original_url).first()
                if existing_url:
                 #    self.created_by=existing_url.created_by
                    return Response("URL already exists")
                self.short_url = self.generate_short_url()

            if ip_address:
                response = requests.get(f'http://ipinfo.io/{ip_address}/json')
                location_data = response.json()
                self.locations.append(location_data)

            super().save(*args, **kwargs)
            return Response("Successfull!!", status=status.HTTP_201_CREATED)

        except Exception as e:
            return response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def generate_short_url(self):
        characters = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(characters) for _ in range(6))
        return short_url

    def __str__(self):
        return self.original_url
