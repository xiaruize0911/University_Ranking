# scripts/scrape_usnews.py
import requests
import json
import sys
import csv
from bs4 import BeautifulSoup

FIELDS = {
    'institution.displayName':"Name",
    'institution.schoolType':"Type",
    'institution.state':"State",
    'institution.city':"City",
    'institution.zip':"Zip",
    'institution.region':"Region",
    'institution.isPublic':"isPublic",
    'institution.institutionalControl':"Institution_Control",
    'institution.primaryPhotoCardLarge':"Photo",
    'ranking.sortRank':"Rank",
    'searchData.actAvg.rawValue':"ACT_Average",
    'searchData.percentReceivingAid.rawValue':"Aid",
    'searchData.acceptanceRate.rawValue':"Acceptance Rate",
    'searchData.tuition.rawValue':"Tuition",
    'searchData.hsGpaAvg.rawValue':"GPA_Average",
    'searchData.engineeringRepScore.rawValue':"Engineering Reputation Score",
    'searchData.parentRank.rawValue':"Parent_Rank",
    'searchData.enrollment.rawValue':"Enrollment",
    'searchData.businessRepScore.rawValue':"Business Reputation Score",
    'searchData.satAvg.rawValue':"SAT",
    'searchData.costAfterAid.rawValue':"Cost After Aid",
    'searchData.testAvgs.displayValue.0.value':"SAT_Range",
    'searchData.testAvgs.displayValue.1.value':"ACT_Range",
    'blurb':"Blurb"
}

def get_value(school, field):
    # print(f"Extracting field: {field}")
    value = school
    for key in field.split('.'):
        realKey = int(key) if key.isdigit() else key
        try:
            value = value[int(key) if key.isdigit() else key]
        except:
            raise Exception(f"Field '{field}' not found in the school data when trying {key}.")
            
    return value


def scrape_usnews():
    base_url = "https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page="
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
        for school in json_data['data']['items']:
            school_data = []
            for field, name in FIELDS.items():
                value = get_value(school, field)
                if value is not None:
                    school_data.append(value)
                else:
                    school_data.append("N/A")
            data_writer.writerow(school_data)
        print(f"Scraped page {pageid} successfully.")
        
    
with open('data.csv', 'w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    colNames = [name for _, name in FIELDS.items()]
    data_writer.writerow(colNames)
    scrape_usnews()