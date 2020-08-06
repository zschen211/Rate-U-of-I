from google_images_download import google_images_download
import os
import pandas as pd

def downloader():
    df_list = [pd.read_csv('excel/cafe.csv',encoding = 'gb18030')]
    place_list = ['cafe']
    idx = 0
    for df in df_list:
        path = "./image/" + place_list[idx] + '/'
        for name in df['Name']:
            name = name.replace('/', ' ')
            name = name.replace('|', '')
            dir_name = path
            
            # download images
            arguments = {
                "keywords": name,
                "limit": 10,
                "output_directory": dir_name,
                "chromedriver": "C:/Users/tony0/AppData/Local/Temp/Rar$EXa18636.20801/chromedriver.exe",
                "print_urls":True
            }

            response = google_images_download.googleimagesdownload()
            absolute_image_paths = response.download(arguments)
            print(absolute_image_paths)

        idx += 1


def combiner():
    df_list = [pd.read_csv('excel/restaurant.csv'), pd.read_csv('excel/cafe.csv',encoding = 'gb18030'), pd.read_csv('excel/hotel.csv'), pd.read_csv('excel/night life.csv')]
    place_list = ['restaurant', 'cafe', 'hotel', 'night life']

    print(os.getcwd())

    for i in range(4):
        df = df_list[i]
        place = place_list[i]
        img_path = []
        for name in df['Name']:
            path = './image/' + place + '/' + name
            if os.path.isdir(path):
                print('path added!')
                img_path.append('static/img' + path[7:])
            else:
                print(path)
                img_path.append('')

        df['Img_path'] = img_path
        df.to_csv(place + '.csv')
            

combiner()