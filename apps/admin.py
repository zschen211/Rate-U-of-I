from django.contrib import admin
from apps.models import Place, User, Rating, Comment, Friend, History

# Register your models here.
admin.site.register(Place)
admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(History)