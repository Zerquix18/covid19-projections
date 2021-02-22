#!/usr/bin/python3.8
# author: Luis A. Martínez <contact@zerquix18.com>

import os
import tabula
import json

base = os.path.dirname(os.path.abspath(__file__)) + '/reports/'
file_list = sorted(os.listdir(base), key = lambda x: int(x.split('.')[0]))

for file_name in file_list:  
  file_path = base + file_name
  report_number = int(file_name.split('.')[0])

  if report_number == 1:
    result = tabula.read_pdf(file_path, pages=2, area=(454.028, 52.403, 654.458, 359.168), output_format="json")

    for row in result[0]['data']:
      province = row[0]['text']

      if province in ['Total', 'Provincia']:
        continue

      cases = int(row[4]['text'])

  break
  