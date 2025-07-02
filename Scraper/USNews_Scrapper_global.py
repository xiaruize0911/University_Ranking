# scripts/scrape_usnews.py
import requests
import json
import sys
import csv
from bs4 import BeautifulSoup
import USNews_detailed_info_parse as parse

FIELDS = {
    'name': 'Name',
    'ranks.0.value': 'Rank',
    'stats.0.value': 'Global Score from US News',
    'image_url.large': 'Image',
    'blurb': 'Description',
    'city': 'City',
    'country_name': 'Country',
    'three_digit_country_code': 'Country Code',
}

def get_value(school, field):
    # print(f"Extracting field: {field}")
    value = school
    for key in field.split('.'):
        realKey = int(key) if key.isdigit() else key
        try:
            value = value[int(key) if key.isdigit() else key]
        except:
            # raise Exception(f"Field '{field}' not found in the school data when trying {key}.(School: {school})")
            return "N/A"
            
    return value

merged_json = []

def scrape_usnews():
    base_url = "https://www.usnews.com/education/best-global-universities/api/search?page="
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0'
    }
    pageid = 0
    while True:
        pageid += 1
        # if pageid > 3:
        #     break
        resp = requests.get(base_url+str(pageid), headers=HEADERS)
        if resp.status_code != 200:
            print(f"Failed to retrieve data for page {pageid}. Status code: {resp.status_code}")
            break
        json_data = resp.json()
        # print(json_data['items'])
        # with open(f'data_page_{pageid}.json', 'w') as json_file:
        #     json.dump(json_data, json_file, indent=4)
        for school in json_data['items']:
            result_json = []
            school_data = []
            # print(school.keys())
            for field, name in FIELDS.items():
                value = get_value(school, field)
                if value is not None:
                    school_data.append(value)
                    result_json.append({name: value})
                else:
                    school_data.append("N/A")
            detailed_info = parse.parse_university(get_value(school, 'url'))
            for field, value in detailed_info.items():
                result_json.append({field: value})
            data_writer.writerow(school_data)
            merged_json.append(result_json)
        print(f"Scraped page {pageid} successfully.")

with open('data.csv', 'w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    colNames = [name for _, name in FIELDS.items()]
    data_writer.writerow(colNames)
    scrape_usnews()
with open(f'usnews_detailed_data.json', 'a') as json_file:
    json.dump(merged_json, json_file, indent=4)
    json_file.write('\n')