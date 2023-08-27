from django.shortcuts import render, redirect
import uuid
from .models import Url
from django.http import HttpResponse
# Create your views here.


def index(req):
    return render(req, 'urlshortner/index.html')


def create(req):
    if req.method == 'POST':
        orginal_url = req.POST['link']
        short_url = req.POST['short_link']
        if Url.objects.filter(orginal_url=orginal_url).exists():
            str = "Shortend url already exists: localhost:8000/" + \
                Url.objects.get(orginal_url=orginal_url).shortned_url
        elif Url.objects.filter(shortned_url=short_url).exists():
            str = "Short Url already taken"
        else:
            new_url = Url(orginal_url=orginal_url, shortned_url=short_url)
            new_url.save()
            str = "localhost:8000/" + short_url
        return HttpResponse(str)


def go(req, pk):
    url_details = Url.objects.get(shortned_url=pk)
    url_details.no_of_clicks += 1
    url_details.save()
    return redirect(url_details.orginal_url)
