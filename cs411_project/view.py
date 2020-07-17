from django.http import HttpResponse
from django.shortcuts import render

def main(request):
    return render(request,'mainpage.html')

def login(request):
    return render(request,'login_page.html')