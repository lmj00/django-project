import csv
import os
import django
import sys


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_project.settings')
django.setup()


from member.models import *

CSV_PATH_PRODUCTS = './extract.csv'


with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
            AddressCSV.objects.create(
                code = row[0],
                name = row[1],
                status = row[2]
            )

