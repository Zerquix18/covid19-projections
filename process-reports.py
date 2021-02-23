#!/usr/bin/python3.8
# author: Luis A. Martínez <contact@zerquix18.com>

import os
from tabula.io import read_pdf
import PyPDF2
import json
import sys

provinces = [
  { "name": "Distrito Nacional", "population": 0, "cases": [] },
  { "name": "Azua", "population": 0, "cases": [] },
  { "name": "Baoruco", "population": 0, "cases": [] },
  { "name": "Barahona", "population": 0, "cases": [] },
  { "name": "Dajabón", "population": 0, "cases": [] },
  { "name": "Duarte", "population": 0, "cases": [] },
  { "name": "Elías Piña", "population": 0, "cases": [] },
  { "name": "El Seibo", "population": 0, "cases": [] },
  { "name": "Espaillat", "population": 0, "cases": [] },
  { "name": "Independencia", "population": 0, "cases": [] },
  { "name": "La Altagracia", "population": 0, "cases": [] },
  { "name": "La Romana", "population": 0, "cases": [] },
  { "name": "La Vega", "population": 0, "cases": [] },
  { "name": "María Trinidad Sánchez", "population": 0, "cases": [] },
  { "name": "Monte Cristi", "population": 0, "cases": [] },
  { "name": "Pedernales", "population": 0, "cases": [] },
  { "name": "Peravia", "population": 0, "cases": [] },
  { "name": "Puerto Plata", "population": 0, "cases": [] },
  { "name": "Hermanas Mirabal", "population": 0, "cases": [] },
  { "name": "Samaná", "population": 0, "cases": [] },
  { "name": "San Cristóbal", "population": 0, "cases": [] },
  { "name": "San Juan", "population": 0, "cases": [] },
  { "name": "San Pedro de Macorís", "population": 0, "cases": [] },
  { "name": "Sánchez Ramírez", "population": 0, "cases": [] },
  { "name": "Santiago", "population": 0, "cases": [] },
  { "name": "Santiago Rodríguez", "population": 0, "cases": [] },
  { "name": "Valverde", "population": 0, "cases": [] },
  { "name": "Monseñor Nouel", "population": 0, "cases": [] },
  { "name": "Monte Plata", "population": 0, "cases": [] },
  { "name": "Hato Mayor", "population": 0, "cases": [] },
  { "name": "San José de Ocoa", "population": 0, "cases": [] },
  { "name": "Santo Domingo", "population": 0, "cases": [] },
  { "name": "No especificado", "population": 0, "cases": [] },
]

# cases = {
#  source_report: int;
#  date: string;
#  total_cases: int;
#  total_deaths: int;
#  total_recovered: int;
#  total_tests: int|None;
#  positivity: float|None;
# }

def get_province_index(name):
  for index, province in enumerate(provinces):
    if province['name'] == name:
      return index

  return -1

def get_date(page_text, number):
  lines = page_text.split("\n")
  for line in lines:
    if line.startswith('FECHA'):
      [dd, mm, yyyy] = line.replace('FECHA: ', '').split('/')
      return '%s/%s/%s' % (yyyy, mm, dd)

base = os.path.dirname(os.path.abspath(__file__)) + '/reports/'
file_list = sorted(os.listdir(base), key = lambda x: int(x.split('.')[0]))

for file_name in file_list:  
  file_path = base + file_name
  report_number = int(file_name.split('.')[0])
  file_reader = PyPDF2.PdfFileReader(file_path)
  
  date = get_date(file_reader.getPage(1).extractText(), report_number)

  ## so here i go covering case by case because they neither provide an API
  ## nor they have consistency writing documents...

  if report_number < 13:
    continue

  print("Processing %d ..." % report_number)

  if report_number == 1:
    result = read_pdf(file_path, pages=2, area=(454.028, 52.403, 654.458, 359.168), output_format="json")

    for row in result[0]['data']:
      province = row[0]['text'].strip()

      if province in ['Total', 'Provincia', '']:
        continue

      cases = int(row[4]['text'])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': 0,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 2:
    result = read_pdf(file_path, pages = 2, area = (232.002,56.0,681.822,356.645), output_format="json")
    
    data = result[0]['data'][3:]

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[-1]['text'])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': 0,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number > 2 and 4 > report_number:
    result = read_pdf(file_path, pages = 2, area = (239.063,56.228,681.998,319.388), output_format="json")
    
    data = result[0]['data'][1:]

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[-1]['text'])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': 0,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number > 3 and 11 > report_number:
    result = read_pdf(file_path, pages = 2, area = (239.063,56.228,681.998,319.388), output_format="json")
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'])
      deaths = int(row[2]['text'])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 11:
    result = read_pdf(file_path, pages = 2, area = (231.413,51.638,688.118,362.228), output_format="json")
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1].strip())
      deaths = int(row[2]['text'].strip())

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 12:
    result = read_pdf(file_path, pages = 2, area = (229.883,53.168,690.413,356.873), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1])
      deaths = int(row[2]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))

      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 13:
    result = read_pdf(file_path, pages = 2, area = (220.703,37.868,690.413,330.098), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1])
      deaths = int(row[2]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))
      
      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 14:
    result = read_pdf(file_path, pages = 2, area = (226.823,52.403,688.883,309.443), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1])
      deaths = int(row[2]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))
      
      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 15:
    result = read_pdf(file_path, pages = 2, area = (232.943,53.168,685.823,312.503), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1])
      deaths = int(row[2]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))
      
      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 16:
    result = read_pdf(file_path, pages = 2, area = (231.413,52.403,694.238,320.918), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[1]['text'].split(' ')[-1])
      deaths = int(row[2]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))
      
      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 17:
    result = read_pdf(file_path, pages = 2, area = (232.943,53.933,695.003,313.268), output_format="json", stream=True)
    
    data = result[0]['data']

    for row in data:
      province = ' '.join(row[0]['text'].split(' ')[1:]).strip()

      if province in ['Total', 'Provincia', '']:
        continue
      
      cases = int(row[2]['text'].split(' ')[-1])
      deaths = int(row[4]['text'].split(' ')[-1])

      index = get_province_index(province)

      if index == -1:
        sys.exit("could not find index for %s (%d)" % (province, report_number))
      
      provinces[index]['cases'].append({
        'source_report': report_number,
        'date': date,
        'total_cases': cases,
        'total_deaths': deaths,
        'total_recovered': 0,
        'total_tests': None,
        'positivity': None,
      })

  if report_number == 18:
    break

print(provinces)
