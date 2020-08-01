from django.shortcuts import render, redirect
from .models import Place, User, Comment, Friend, Rating, History
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection, transaction
import os
import shutil
import math
import numpy as np
from textblob import TextBlob
from PIL import Image



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

            # automatically login in
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)

        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "signup_page.html", {"form":form})


def user_profile(request):
    implicit_rating()
    username = request.user.username
    user_info = User.objects.raw(
        "SELECT * FROM apps_user WHERE username = %s", [username]
    )[0]
    # get friend list
    current_user = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [username])[0]
    friends = Friend.objects.get(current_user=current_user).users.all()
    # get profile image
    image_path = 'static/img/avatar/' + user_info.username + '/'
    try:
        files = os.listdir(image_path)
        profile_image = files[0]
        profile_image = image_path + profile_image
        return render(request, "user_profile.html", {'user_info': user_info, 'profile_image': profile_image[7:], 'friends':friends})
    except:
        return render(request, "user_profile.html", {'user_info': user_info, 'profile_image': None, 'friends':friends})


def edit_profile(request):
    if request.POST:
        username = request.user.username
        age = request.POST.get('age', None)
        gender = request.POST.get('gender', None)
        country = request.POST.get('country', None)
        ethnicity = request.POST.get('ethnicity', None)
        avatar = request.FILES.get('avatar', None)
        biography = request.POST.get('biography', None)

        # update model
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE apps_user SET age=%s, gender=%s, country=%s, ethnicity=%s, biography=%s WHERE username=%s", [age, gender, country, ethnicity, biography, username]
        )
        transaction.commit()

        # update avatar
        if os.path.isdir('static/img/avatar/'+username):
            shutil.rmtree('static/img/avatar/'+username)
        os.mkdir('static/img/avatar/'+username)
        with open('static/img/avatar/' + username +'/'+ str(avatar), 'wb') as f:
            for line in avatar:
                f.write(line)
        
        return redirect('profile')

    return render(request, 'edit_info.html')


def get_img(path):
    img_list = os.listdir(path)
    return img_list


def place_detail(request, place_name):
    place = Place.objects.raw(
            "SELECT * FROM apps_place WHERE placeName=%s", [place_name]
    )[0]
    comment_list = User.objects.raw('SELECT * FROM apps_comment c JOIN apps_user u ON c.userID_id = u.userID WHERE c.placeID_id=%s', [place.placeID])
    img_list = get_img(place.img_path)
    thumbnail = place.img_path[7:] + '/' + img_list[3]
    # thumbnail = None
    username = request.user.username
    user_object = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [username])[0]
    userID = user_object.userID

    # update view history
    cursor = connection.cursor()
    try: 
        history = History.objects.raw('SELECT * FROM apps_history WHERE userID_id=%s AND placeID_id=%s', [userID, place.placeID])[0]
        cursor.execute('UPDATE apps_history SET view_count=view_count+1 WHERE userID_id=%s AND placeID_id=%s', [userID, place.placeID])
    except:
        cursor.execute('INSERT INTO apps_history(userID_id, placeID_id, view_count) VALUES(%s, %s, %s)', [userID, place.placeID, 1])
    transaction.commit()

    if request.POST:
        if request.user.is_authenticated:
            content = request.POST.get('comment_content')
            deletion = request.POST.get('delete')
            rate = request.POST.get('rate')

            # user rating
            existed_rating = Rating.objects.raw('SELECT * FROM apps_rating WHERE userID_id=%s AND placeID_id=%s', [userID, place.placeID])
            flag1 = 0
            try:
                temp = existed_rating[0]
                flag1 = 1
            except:
                flag1 = 0
            if rate:
                # add or modify rating
                cursor = connection.cursor()
                if not flag1:
                    cursor.execute('INSERT INTO apps_rating(userID_id, placeID_id, user_rating) VALUES(%s, %s, %s)', [userID, place.placeID, rate])
                else:
                    cursor.execute('UPDATE apps_rating SET user_rating=%s WHERE userID_id=%s AND placeID_id=%s', [rate, userID, place.placeID])
                transaction.commit()

            # comment deletion
            if deletion:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM apps_comment WHERE userID_id=%s AND placeID_id=%s', [userID, place.placeID])
                transaction.commit()

            # comment functionality
            existed_comment = Comment.objects.raw('SELECT * FROM apps_comment WHERE userID_id=%s AND placeID_id=%s', [userID, place.placeID])
            flag2 = 0
            try:
                temp = existed_comment[0]
                flag2 = 1
            except:
                flag2 = 0
            if content:
                if not flag2:
                    # add comment to database
                    cursor = connection.cursor()
                    cursor.execute('INSERT INTO apps_comment(userID_id, placeID_id, user_comment) VALUES(%s, %s, %s)', [userID, place.placeID, content])
                    transaction.commit()
                else:
                    return HttpResponse('Only one comment is allowed for each place!')
                # get context
                comment_list = User.objects.raw('SELECT * FROM apps_comment c JOIN apps_user u ON c.userID_id = u.userID WHERE c.placeID_id=%s', [place.placeID])
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':thumbnail})
            else:
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':thumbnail})
        else:
            return redirect("/login/")
    else:
        return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':thumbnail})


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


def implicit_rating():
    ratings = Rating.objects.raw('SELECT * FROM apps_rating')
    comments = Comment.objects.raw('SELECT * FROM apps_comment')
    views = History.objects.raw('SELECT * FROM apps_history')
    item_count = Place.objects.count()
    user_max_id = User.objects.raw('SELECT * FROM apps_user')[-1].userID

    # generate matrix
    matrix = [[0 for j in range(user_max_id)] for i in range(item_count)]
    for v in views:
        i = v.placeID_id
        j = v.userID_id-1
        matrix[i][j] += v.view_count

    for r in ratings:
        i = r.placeID_id
        j = r.userID_id
        rate = r.user_rating
        if rate == 3:
            matrix[i][j] += 10
        if rate == 4:
            matrix[i][j] += 20
        if rate == 5:
            matrix[i][j] += 30

    for c in comments:
        i = c.placeID_id
        j = c.userID_id
        blob = TextBlob(c.user_comment)
        if blob.sentiment.polarity > 0:
            matrix[i][j] += 50*blob.sentiment.polarity

    return matrix


def average_inter_cluster_distance(c1, c2):
    denominator = 0
    N1 = len(c1)
    N2 = len(c2)
    for m in range(N1):
        for n in range(N2):
            d = np.array(c1[m]) - np.array(c2[n])
            denominator += np.inner(d,d)

    return np.sqrt(denominator/(N1*N2))