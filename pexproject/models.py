from django.db import models

class Flightdata(models.Model):
    rowid = models.AutoField(primary_key=True)
    scrapetime = models.DateTimeField()
    searchkeyid = models.IntegerField ()
    flighno = models.CharField(max_length=100)
    stoppage = models.CharField(max_length=100)
    stoppage_station = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure = models.TimeField('Alarm')
    arival = models.TimeField('Alarm')
    duration = models.CharField(max_length=100)
    maincabin = models.CharField(max_length=100)
    firstclass = models.CharField(max_length=100)
    cabintype1 =  models.CharField(max_length=100)
    cabintype2 =  models.CharField(max_length=100)
# Create your models here.
class Airports(models.Model):
    airport_id = models.IntegerField (primary_key=True)
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=255)
    cityCode = models.CharField(max_length=50)
    cityName = models.CharField(max_length=200)
    countryName = models.CharField(max_length=200)
    countryCode = models.CharField(max_length=200)
    timezone = models.CharField(max_length=8)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=200)
    numAirports = models.IntegerField()
    city = models.BooleanField(default=True)
    
    
class Searchkey(models.Model):
    searchid = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    traveldate = models.DateField(max_length=50)
    scrapetime = models.DateTimeField(max_length=50)