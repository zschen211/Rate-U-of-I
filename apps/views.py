from django.shortcuts import render, redirect
from .models import Place, User, Comment, Friend
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
            "(SELECT * FROM apps_place WHERE placeName LIKE %s OR types LIKE %s ORDER BY rating DESC) UNION (SELECT * FROM apps_place WHERE description IS NOT NULL AND description<>'' AND description LIKE %s ORDER BY rating DESC)", [content, content, content]
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


def user_profile(request):
    username = request.user.username
    user_info = User.objects.raw(
        "SELECT * FROM apps_user WHERE username = %s", [username]
    )
    return render(request, "user_profile.html", {'user_info': user_info[0]})


def edit_profile(request):
    if request.POST:
        username = request.user.username
        age = request.POST.get('age', None)
        gender = request.POST.get('gender', None)
        country = request.POST.get('country', None)
        ethnicity = request.POST.get('ethnicity', None)

        # update model
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE apps_user SET age=%s, gender=%s, country=%s, ethnicity=%s WHERE username=%s", [age, gender, country, ethnicity, username]
        )
        transaction.commit()
        return redirect('profile')

    return render(request, 'edit_info.html')


def place_detail(request, place_name):
    place = Place.objects.raw(
            "SELECT * FROM apps_place WHERE placeName=%s", [place_name]
    )[0]
    comment_list = User.objects.raw('SELECT * FROM apps_comment c JOIN apps_user u ON c.userID_id = u.userID WHERE c.placeID_id=%s', [place.placeID])

    if request.POST:
        if request.user.is_authenticated:
            content = request.POST.get('comment_content')
            deletion = request.POST.get('delete')
            username = request.user.username
            user_object = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [username])[0]
            userID = user_object.userID

            if deletion:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM apps_comment WHERE userID_id=%s', [userID])
                transaction.commit()

            if content:
                # add comment to database
                cursor = connection.cursor()
                cursor.execute('INSERT INTO apps_comment(userID_id, placeID_id, user_comment) VALUES(%s, %s, %s)', [userID, place.placeID, content])
                transaction.commit()
                # get context
                comment_list = User.objects.raw('SELECT * FROM apps_comment c JOIN apps_user u ON c.userID_id = u.userID WHERE c.placeID_id=%s', [place.placeID])
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list})
            else:
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list})
        else:
            return redirect("/login/")
    else:
        return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list})


def add_friend(request):
    if request.POST:
        username = request.POST.get('username')
        current_username = request.user.username
        try:
            added_user = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [username])[0]
            current_user = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [current_username])[0]
            Friend.make_friends(current_user, added_user)
            # print(Friend.objects.get(current_user=current_user).users.all())
            return HttpResponse('Added successfully!')
        except:
            return HttpResponse('Username does not exist!')
    return render(request, 'add_friend.html')