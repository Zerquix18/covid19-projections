#!/usr/bin/python3.8
## author: Luis A. Martínez <contact@zerquix18.com>

import requests
from bs4 import BeautifulSoup
import re
import os

def fix_link(link):
  link = link.strip().strip('/').replace('Boletín', 'Boletin')

  if not link.endswith('.pdf'): # 61 has this problem
    link = link + '.pdf' 
  
  if link.endswith('pdf.pdf'): # 49 has this problem
    link = link.replace('pdf.pdf', '.pdf')

  have_i_accute = ["171", "172", "173", "174", "175", "176", "177", "178"]
  have_trailing_dash = ["37", "38", "39"]
  dont_require_covid19 = ["37", "50", "51", "65", "75"]
  do_require_covid19 = ["137", "151", "237"]

  for exception in have_i_accute:
    if exception in link:
      link = link.replace('Boletin', 'Boletín')
  
  for exception in have_trailing_dash:
    if exception in link:
      link = link.replace('-.pdf', '.pdf')
  
  for exception in dont_require_covid19:
    if exception in link:
      link = link.replace('-COVID-19.pdf', '.pdf')

  for exception in do_require_covid19:
    if exception in link:
      link = link.replace('.pdf', '-COVID-19.pdf')

  return link

def get_report_number_from_link(link):
  filename = link.split('/')[-1].replace('COVID-19', '')
  report_number = int(re.findall(r'\d+', filename)[0])
  return report_number

def get_province_index(provinces, name):
  for index, province in enumerate(provinces):
    if province['name'] == name:
      return index

  return -1


headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-encoding': 'accept-encoding: gzip, deflate, br',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

response = requests.get('https://www.msp.gob.do/web/?page_id=6948', headers = headers)
soup = BeautifulSoup(response.content, 'html.parser')

report_list = soup.select('[rel="noopener noreferrer"]')
links = list(set(map(lambda a: 'https://www.msp.gob.do/' + fix_link(a['href']), report_list)))

## these 2 are linked WRONG on the website or are just not listed at all in the HTML
links.append("https://www.msp.gob.do/web/wp-content/uploads/2020/06/Boletin-especial-88.pdf")
links.append("https://www.msp.gob.do/web/wp-content/uploads/2020/08/Boletin-especial-150-COVID-19.pdf")

# 194 and 319 don't exist on the website (tried every naming convention)
# but they do exist on Twitter https://twitter.com/search?q=from%3Asaludpublicard%20194%20OR%20319&src=typed_query&f=live
# have to be copied manually :( 

most_recent_one = 'https://www.msp.gob.do/' + fix_link(soup.select('iframe')[0]['data-src'])
links.append(most_recent_one)

## the parsing method will depend on the report number so
## inevitably we'll need to extract it from the URL

reports = list(map(lambda link: { 'link': link, 'number': get_report_number_from_link(link) }, links))
reports = sorted(reports, key = lambda report: report['number'])

total_reports = len(reports)

for report in reports:
  link = report['link']
  number = report['number']

  print('downloading report %d out of %d' % (number, total_reports))

  response = requests.get(link)
  filename = '%s/reports/%d.pdf' % (os.path.dirname(os.path.abspath(__file__)), number)

  with open(filename, 'wb') as file:
    file.write(response.content)

print('my job is done')
