import pandas as pd, numpy as np
import requests 
import json
import time

coordinates = '40.1254021,-88.2488426'
keywords = ['restaurant','cafe','hotel','night life']
radius = '5000'
api_key = 'AIzaSyDUDviS4HwzicDYlRAKCednTvd9wN5QRdE'

for keyword in keywords:
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+coordinates+'&radius='+str(radius)+'&keyword='+str(keyword)+'&key='+str(api_key)
    print(url)

    data_list = []


    while True:
        r = requests.get(url)
        j = json.loads(r.text)
        result = j['results']
        for place in result:
            name = place['name']
            status = place['business_status']

            # mix types into one string
            types = place['types']
            tmp_str = ''
            for tp in types:
                if tp != 'point_of_interest' or tp != 'establishment':
                    tmp_str += (tp + ' ')
            types = tmp_str

            vicinity = place['vicinity']
            if 'price_level' in place:
                price_level = place['price_level']
            else:
                price_level = 0
                
            rating = place['rating']
            user_ratings_num = place['user_ratings_total']
            latitude = place['geometry']['location']['lat']
            longitude = place['geometry']['location']['lng']
            data_list.append([name,status,types,vicinity,price_level,rating,user_ratings_num])

        time.sleep(3)

        if 'next_page_token' not in j: 
            break
        else:
            next_page_token = j['next_page_token']
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+str(api_key)+'&pagetoken='+str(next_page_token)
        

    df = pd.DataFrame(data_list, columns=['Name', 'Business_Status', 'Types', 'Vicinity', 'Price_level', 'rating', 'user_ratings_num'])
    
    df.to_csv(keyword + '.csv')