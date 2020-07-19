from django.shortcuts import render, redirect
from .models import Place, User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse


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
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                new_user = User.objects.raw(
                    "SELECT * FROM User WHERE username = %s", [username]
                )
                return HttpResponse('User already exists!')
            except:
                form.save()
                return HttpResponseRedirect('/login/')
        else:
            return render(request, 'signup_page.html', {'form':form})
    else:
        form = RegisterForm()
        return render(request, 'signup_page.html', {'form':form})


def user_login(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # print(password)
        try:
            user = User.objects.get(username = username)
        except:
            return render(request, 'login_page.html')
        if user.password == password:
            return redirect('/')
        else:
            return HttpResponse('Wrong password!')
    return render(request, 'login_page.html')
