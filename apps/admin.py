from django.contrib import admin
from apps.models import Place, User, Rating

# Register your models here.
admin.site.register(Place)
admin.site.register(User)
admin.site.register(Rating)