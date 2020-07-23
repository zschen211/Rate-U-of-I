from django.shortcuts import render, redirect
from .models import Place, User
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection, transaction


# Create your views here.
def search(request):
    content = request.GET.get('search_content')
    if content:
        content = '%' + content + '%'
        place_list = Place.objects.raw(
            "SELECT * FROM apps_place WHERE placeName LIKE %s OR types LIKE %s ORDER BY rating", [content, content]
        )
        return render(request, 'results.html', {'place_list':place_list})


def user_register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            gender = form.cleaned_data['gender']
            country = form.cleaned_data['country']
            age = form.cleaned_data['age']
            ethnicity = form.cleaned_data['ethnicity']
            print(username, password, gender, country, age, ethnicity)

            # save data to model
            cursor = connection.cursor()
            cursor.execute("INSERT INTO apps_user(username, password, gender, country, ethnicity, age) VALUES(%s, %s, %s, %s, %s, %s)", [username, password, gender, country, ethnicity, age])
            transaction.commit()

        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "signup_page.html", {"form":form})

