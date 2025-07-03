import requests
from bs4 import BeautifulSoup
import re

ALIASES = {
    'mit': 'massachusetts institute of technology',
    'caltech': 'california institute of technology',
    'ucb': 'university of california berkeley',
    'stanford': 'stanford university',
    # Add more aliases as needed
}

def normalize_name(name: str) -> str:
    # Lowercase
    name = name.lower()
    # Remove text in parentheses, like "(MIT)"
    name = re.sub(r'\(.*?\)', '', name)
    # Remove punctuation
    name = re.sub(r'[^\w\s]', '', name)
    # Normalize spaces
    name = re.sub(r'\s+', ' ', name)
    if name in ALIASES:
        # If the name is an alias, replace it with the full name
        name = ALIASES[name]
    return name.strip()

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0'
}
def parse_university(url):
    print(f"Fetching data from {url}...")
    resp = requests.get(url,headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    with open('test.html', 'wb+') as f:
        f.write(resp.content)

    result = {}

    # 1. University name
    name_tag = soup.find(class_ ='Heading-sc-1w5xk2o-0 iErXUE')
    result['name'] = name_tag.text.strip() if name_tag else None

    # 2. University data
    for data_tag in soup.find_all(class_='Box-w0dun1-0 DataRow__Row-sc-1udybh3-0 egPJfu keLhhz'):
        tag = data_tag.find(class_='Paragraph-sc-1iyax29-0 fZPEMD')
        value = data_tag.find(class_='Paragraph-sc-1iyax29-0 iKkzvP')
        result[tag.text.strip()] = value.text.strip()

    # Subject rankings
    for subject_tag in soup.find_all(class_='RankList__ListItem-sc-2xewen-1 dofuo rank-list-item'):
        try:
            subject_name = subject_tag.find(class_='RankList__RankLink-sc-2xewen-3 kUTsMg has-badge').find('strong').find_next('strong')
        except:
            break
        rank = subject_tag.find(class_='RankList__Rank-sc-2xewen-2 ktVaRA ranked has-badge').text.strip()
        rank = int(rank[1:])
        subject_name = normalize_name(subject_name.text.strip())
        result[subject_name] = rank
    
    return result

# url = 'https://www.usnews.com/education/best-global-universities/harvard-university-166027'
# data = parse_university(url)
# import json
# print(json.dumps(data, indent=2))
