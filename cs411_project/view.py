from django.http import HttpResponse
from django.shortcuts import render
from apps.models import Place
import os

def main(request):
    return render(request,'mainpage.html')


def get_img(path):
    img_list = os.listdir(path)
    return img_list


def restaurant_summary(request):
    if request.POST:
        content = '%' + 'restaurant' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        # count query
        count = Place.objects.raw('(SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE placeName LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE types LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE description LIKE %s GROUP BY business_status)', [content, content, content])
        status_count = {}
        for c in count:
            if c.business_status not in status_count:
                status_count[c.business_status] = c.cnt
            else:
                status_count[c.business_status] += c.cnt
        status = []
        for s in status_count:
            status.append((s, status_count[s]))

        result_list = []
        for i in range(len(place_list)):
            place = place_list[i]
            img_list = get_img(place.img_path)
            for img in img_list:
                if img[0:9] == 'thumbnail': 
                    result_list.append((place.placeName, place.vicinity, place.rating, place.price_level, place.business_status, place.description, place.img_path[7:] + '/' + img))

        return render(request, 'results.html', {'place_list':result_list, 'status':status})
    return render(request, 'restaurant_summary.html')

def cafe_summary(request):
    if request.POST:
        content = '%' + 'cafe' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        # count query
        count = Place.objects.raw('(SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE placeName LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE types LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE description LIKE %s GROUP BY business_status)', [content, content, content])
        status_count = {}
        for c in count:
            if c.business_status not in status_count:
                status_count[c.business_status] = c.cnt
            else:
                status_count[c.business_status] += c.cnt
        status = []
        for s in status_count:
            status.append((s, status_count[s]))

        result_list = []
        for i in range(len(place_list)):
            place = place_list[i]
            img_list = get_img(place.img_path)
            for img in img_list:
                if img[0:9] == 'thumbnail': 
                    result_list.append((place.placeName, place.vicinity, place.rating, place.price_level, place.business_status, place.description, place.img_path[7:] + '/' + img))

        return render(request, 'results.html', {'place_list':result_list, 'status':status})
    return render(request, 'milktea_summary.html')

def hotel_summary(request):
    if request.POST:
        content = '%' + 'lodging' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        # count query
        count = Place.objects.raw('(SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE placeName LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE types LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE description LIKE %s GROUP BY business_status)', [content, content, content])
        status_count = {}
        for c in count:
            if c.business_status not in status_count:
                status_count[c.business_status] = c.cnt
            else:
                status_count[c.business_status] += c.cnt
        status = []
        for s in status_count:
            status.append((s, status_count[s]))

        result_list = []
        for i in range(len(place_list)):
            place = place_list[i]
            img_list = get_img(place.img_path)
            for img in img_list:
                if img[0:9] == 'thumbnail': 
                    result_list.append((place.placeName, place.vicinity, place.rating, place.price_level, place.business_status, place.description, place.img_path[7:] + '/' + img))

        return render(request, 'results.html', {'place_list':result_list, 'status':status})
    return render(request, 'hotel_summary.html')

def nightbar_summary(request):
    if request.POST:
        content = '%' + 'bar' + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE types LIKE %s ORDER BY rating DESC", [content]
        )
        # count query
        count = Place.objects.raw('(SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE placeName LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE types LIKE %s GROUP BY business_status) UNION (SELECT *, COUNT(placeID) AS cnt FROM apps_place WHERE description LIKE %s GROUP BY business_status)', [content, content, content])
        status_count = {}
        for c in count:
            if c.business_status not in status_count:
                status_count[c.business_status] = c.cnt
            else:
                status_count[c.business_status] += c.cnt
        status = []
        for s in status_count:
            status.append((s, status_count[s]))

        result_list = []
        for i in range(len(place_list)):
            place = place_list[i]
            img_list = get_img(place.img_path)
            for img in img_list:
                if img[0:9] == 'thumbnail': 
                    result_list.append((place.placeName, place.vicinity, place.rating, place.price_level, place.business_status, place.description, place.img_path[7:] + '/' + img))

        return render(request, 'results.html', {'place_list':result_list, 'status':status})
    return render(request, 'nightbar_summary.html')
