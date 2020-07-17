from django.db import models

# Create your models here.
class Place(models.Model):
    placeName = models.CharField(max_length=200)
    placeID = models.CharField(max_length=50, primary_key=True)
    business_status = models.CharField(max_length=50)
    types = models.CharField(max_length=100)
    vicinity = models.CharField(max_length=100)
    price_level = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    users_rating_num = models.IntegerField(default=0)

class User(models.Model):
    userID = models.AutoField(default=0, primary_key=True)
    username = models.IntegerField(default=0)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    ethnicity = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

class Rating(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE,related_name='+')
    placeID = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='+')
    user_rating = models.FloatField(default=0)



