from django.http import HttpResponse
from django.shortcuts import render

def main(request):
    return render(request,'mainpage.html')

def login(request):
    return render(request,'login_page.html')

def signUp(request):
    return render(request,'signup_page.html')

def restaurant_summary(request):
    return render(request, 'restaurant_summary.html')

def cafe_summary(request):
    return render(request, 'milktea_summary.html')

def hotel_summary(request):
    return render(request, 'hotel_summary.html')

def nightbar_summary(request):
    return render(request, 'nightbar_summary.html')