from django.db import models

# Create your models here.


class Url(models.Model):
    orginal_url = models.CharField(max_length=1000)
    shortned_url = models.CharField(max_length=10)
    no_of_clicks = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default="")
    referrals = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.orginal_url} --> {self.shortned_url}"
