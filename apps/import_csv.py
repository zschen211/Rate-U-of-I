import csv
from apps.models import Place


contSuccess = 0
# Remove all data from Table
# Place.objects.all().delete()

with open('apps/csv/Restaurant.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    print('Loading...')
    for row in spamreader:
        if not Place.objects.filter(placeName=row[0], placeID=row[1]).exists():
            Place.objects.create(placeName=row[0], placeID=row[1], business_status=row[2], types=row[3], vicinity=row[4], price_level=row[5], rating=float(row[6]), users_rating_num=row[7])
            contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')