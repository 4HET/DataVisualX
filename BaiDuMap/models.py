from django.db import models

# Create your models here.
class LatLng(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()