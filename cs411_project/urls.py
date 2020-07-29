"""cs411_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import view
from apps import views
from apps.views import user_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.main, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.user_register, name='signup'),
    path('search/', views.search, name='search'),
    path('profile/', views.user_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit'),
    path('detail/<str:place_name>/', views.place_detail, name='detail'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('restaurant_summary/', view.restaurant_summary, name='restaurant_summary'), 
    path('cafe_summary/', view.cafe_summary, name='cafe_summary'), 
    path('hotel_summary/', view.hotel_summary, name='hotel_summary'), 
    path('nightbar_summary/', view.nightbar_summary, name='nightbar_summary'), 
]
