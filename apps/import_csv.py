import csv
from apps.models import Place


contSuccess = 0
# Remove all data from Table
# Place.objects.all().delete()

with open('apps/csv/night life.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    print('Loading...')
    for row in spamreader:
        if not Place.objects.filter(placeName=row[0]).exists():
            Place.objects.create(placeName=row[0], business_status=row[1], types=row[2], vicinity=row[3], price_level=row[4], rating=float(row[5]), users_rating_num=row[6],desription=row[7],img_path=row[8])
            contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')