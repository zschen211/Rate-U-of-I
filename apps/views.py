from django.shortcuts import render
from .models import Place

# Create your views here.
def search(request):
    content = request.GET.get('search_content')
    if content:
        content = '%' + content + '%'
        place_list = Place.objects.raw(
            "SELECT placeName, placeID FROM apps_place WHERE placeName LIKE %s OR types LIKE %s ORDER BY rating", [content, content]
        )
        # place_list = Place.objects.filter(placeName__icontains=content)
        return render(request, 'results.html', {'place_list':place_list})