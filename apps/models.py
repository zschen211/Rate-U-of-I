from django.db import models

# Create your models here.
class Place(models.Model):
    placeID = models.AutoField(primary_key=True)
    placeName = models.CharField(max_length=200)
    business_status = models.CharField(max_length=50)
    types = models.CharField(max_length=200)
    vicinity = models.CharField(max_length=100)
    price_level = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    users_rating_num = models.IntegerField(default=0)
    description = models.CharField(max_length=400)
    img_path = models.CharField(max_length=250)

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    ethnicity = models.CharField(max_length=20)
    age = models.IntegerField()
    biography = models.CharField(max_length=400, null=True)

class Rating(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE,related_name='+')
    placeID = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='+')
    user_rating = models.FloatField(default=0)

class Comment(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE,related_name='+')
    placeID = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='+')
    user_comment = models.CharField(max_length=1000)

class Friend(models.Model):
    users = models.ManyToManyField('User')
    current_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner', null=True)
    @classmethod
    def make_friends(cls, current_user, added_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(added_friend)
    @classmethod
    def remove_friends(cls, current_user, added_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(added_friend)

class History(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE,related_name='+')
    placeID = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='+')
    view_count = models.IntegerField(default=0)



