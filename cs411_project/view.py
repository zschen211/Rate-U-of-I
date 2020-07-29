from django.http import HttpResponse
from django.shortcuts import render
from apps.models import Place

def main(request):
    return render(request,'mainpage.html')

def restaurant_summary(request):
    if request.POST:
        content = '%' + 'restaurant' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        return render(request, 'results.html', {'place_list':place_list})
    return render(request, 'restaurant_summary.html')

def cafe_summary(request):
    if request.POST:
        content = '%' + 'cafe' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        return render(request, 'results.html', {'place_list':place_list})
    return render(request, 'milktea_summary.html')

def hotel_summary(request):
    if request.POST:
        content = '%' + 'lodging' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        return render(request, 'results.html', {'place_list':place_list})
    return render(request, 'hotel_summary.html')

def nightbar_summary(request):
    if request.POST:
        content = '%' + 'bar' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        return render(request, 'results.html', {'place_list':place_list})
    return render(request, 'nightbar_summary.html')
