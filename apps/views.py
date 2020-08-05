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
            

        # get thumbnail images 
        result_list = []
        for i in range(len(place_list)):
            place = place_list[i]
            img_list = get_img(place.img_path)
            for img in img_list:
                if img[0:9] == 'thumbnail': 
                    result_list.append((place.placeName, place.vicinity, place.rating, place.price_level, place.business_status, place.description, place.img_path[7:] + '/' + img))

        return render(request, 'results.html', {'place_list':result_list, 'status':status})


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
    data = implicit_rating()
    tuple = dissimilarity_matrix(data)
    rec_ids = recommend(request, tuple[0], tuple[1], data)
    # print(rec_ids)
    rec_list = []
    for id in rec_ids:
        id += 1
        place = Place.objects.raw('SELECT * FROM apps_place WHERE placeID=%s', [id])[0]
        img_list = get_img(place.img_path)
        for img in img_list:
            if img[0:9] == 'thumbnail':
                thumbnail = place.img_path[7:] + '/' + img
        
        rec_list.append((place.placeName, thumbnail))

    username = request.user.username
    user_info = User.objects.raw(
        "SELECT * FROM apps_user WHERE username = %s", [username]
    )[0]

    # get friend list
    current_user = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [username])[0]
    try:
        friends = Friend.objects.get(current_user=current_user).users.all()
    except:
        friends = None

    # get profile image
    image_path = 'static/img/avatar/' + user_info.username + '/'

    # get friends' comments list 
    review = User.objects.raw('SELECT * FROM apps_comment LEFT JOIN apps_user ON (apps_comment.userID_id=apps_user.userID)')
    for i in review:
        print(i)
    review_list = []
    if friends:
        friends_id = [ f.userID for f in friends ]
        place_id_list = []
        for r in review:
            if r.userID_id in friends_id:
                tmp_place = Place.objects.raw('SELECT * FROM apps_place WHERE placeID=%s', [r.placeID_id])[0]
                try:
                    tmp_rating = Rating.objects.raw('SELECT * FROM apps_rating WHERE placeID_id=%s AND userID_id=%s', [tmp_place.placeID, r.userID_id])[0].user_rating
                except:
                    tmp_rating = None
                img_list = get_img(tmp_place.img_path)
                for img in img_list:
                    if img[0:9] == 'thumbnail':
                        thumbnail = tmp_place.img_path[7:] + '/' + img
                r_tuple = (tmp_place.placeName, r.username, r.user_comment, tmp_rating, thumbnail)
                review_list.append(r_tuple)

    try:
        files = os.listdir(image_path)
        profile_image = files[0]
        profile_image = image_path + profile_image
        return render(request, "user_profile.html", {'user_info': user_info, 'profile_image': profile_image[7:], 'friends':friends, 'rec':rec_list, 'review':review_list})
    except:
        return render(request, "user_profile.html", {'user_info': user_info, 'profile_image': None, 'friends':friends, 'rec':rec_list, 'review':review_list})


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
    comment_list = User.objects.raw('(SELECT u.userID, c.placeID_id, c.user_comment AS cnt FROM apps_comment c JOIN apps_user u ON c.userID_id = u.userID WHERE c.placeID_id=%s)', [place.placeID])
    img_list = get_img(place.img_path)
    for i in range(len(img_list)):
        img_list[i] = place.img_path[7:] + '/' + img_list[i]
        print(img_list[i])

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
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':img_list})
            else:
                return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':img_list})
        else:
            return redirect("/login/")
    else:
        return render(request, 'place_detailed.html', {'place':place, 'comment_list':comment_list, 'img':img_list})


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

    # generate data
    data = [[0 for j in range(user_max_id)] for i in range(item_count)]
    for v in views:
        i = v.placeID_id-1
        j = v.userID_id-1
        data[i][j] += v.view_count

    for r in ratings:
        i = r.placeID_id-1
        j = r.userID_id-1
        rate = r.user_rating
        if rate == 3:
            data[i][j] += 10
        if rate == 4:
            data[i][j] += 20
        if rate == 5:
            data[i][j] += 30

    for c in comments:
        i = c.placeID_id-1
        j = c.userID_id-1
        blob = TextBlob(c.user_comment)
        if blob.sentiment.polarity > 0:
            data[i][j] += 50*blob.sentiment.polarity

    return data


def dissimilarity_matrix(data):
    data = np.array(data)
    truncated_data = data[~np.all(data == 0, axis=1)]

    common = {}
    i = 0
    for item in truncated_data:
        key = i
        count = np.count_nonzero(item)
        common[key] = count
        i += 1

    matrix = [[0 for i in range(len(truncated_data))] for j in range(len(truncated_data))]
    for i in range(len(matrix)):
        for j in range(i, len(matrix[0])):
            if i == j: 
                continue
            else:
                item1 = truncated_data[i]
                item2 = truncated_data[j]
                count = 0
                for k in range(len(item1)):
                    if item1[k] != 0:
                        if item2[k] != 0:
                            count += 1
                matrix[i][j] = count
                matrix[j][i] = count
        
    # cosine similarity
    for i in range(len(matrix)):
        for j in range(i, len(matrix[0])):
            matrix[i][j] = matrix[i][j]/math.sqrt(common[i]*common[j])
            matrix[j][i] = matrix[i][j]

    similarity = {}
    for i in range(len(matrix)):
        for x in range(len(data)):
            if np.array_equal(data[x],truncated_data[i]): 
                index1 = x
                break 
        similarity[index1] = []
        for j in range(len(matrix)):
            if i != j:
                for y in range(len(data)):
                    if np.array_equal(data[y],truncated_data[j]): 
                        index2 = y
                        break  
                similarity[index1].append((index2, matrix[i][j]))
                
    
    return (matrix, similarity)


def recommend(request, matrix, similarity_dict, data):
    data = np.array(data)
    truncated_data = data[~np.all(data == 0, axis=1)]

    cur_username = request.user.username
    cur_userID = User.objects.raw('SELECT * FROM apps_user WHERE username=%s', [cur_username])[0].userID
    rating_list = data[:,cur_userID-1]
    recommendation = []
    # print(len(rating_list))
    for i in range(len(rating_list)):
        rate = rating_list[i]
        if rate != 0 and i in similarity_dict:
            similar_places = similarity_dict[i]
            for tup in similar_places:
                index = tup[0]
                sim = tup[1]
                if rating_list[index] == 0:
                    score = sim*rating_list[i]
                    recommendation.append((index, score))

    # clean recommendation list
    recommendation = sorted(recommendation, reverse=True)
    for i in range(len(recommendation)):
        recommendation[i] = recommendation[i][0]
    recommendation = set(recommendation)

    # handle cold start
    if len(recommendation) == 0:
        query = Place.objects.raw('SELECT * FROM apps_place ORDER BY rating DESC LIMIT 6')
        recommendation = list(recommendation)
        for place in query:
            recommendation.append(place.placeID)

    return recommendation