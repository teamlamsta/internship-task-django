from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import requests

class UrlShortner(models.Model):
    incoming_url = models.SlugField(unique=True,max_length=200,blank=False)
    outgoing_url = models.URLField(max_length=300,blank=False)
    click_through_counter = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

