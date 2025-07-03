import pandas as pd
import csv
import re
import json

ALIASES = {
    'mit': 'massachusetts institute of technology',
    'caltech': 'california institute of technology',
    'ucb': 'university of california berkeley',
    'stanford': 'stanford university',
    # Add more aliases as needed
}

def process_rank_below_zero(pd: pd):
    pd.replace(to_replace={'-1','-2',-1,-2}, value=None, inplace=True)

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

def merge_dataframes(df1, df2):
    result = pd.merge(df1, df2, on='normalizedName', how='outer',suffixes=('_1', '_2'))
    for col in result.columns:
        if col.endswith('_1'):
            key = col[:-2]
            # print(f'Merging columns: {col} and {key}_2 into {key}')
            result[key] = result[key+'_1'].combine_first(result[key+'_2'])
            result.drop(columns=[col, key+'_2'], inplace=True)
    return result

def load_data():
    # Loading data from CSV files(USNews US University Rankings and QS World University Rankings)
    QS_data = pd.read_csv('data/2026_QS_World_University_Rankings_1.0.csv')
    process_rank_below_zero(QS_data)
    USNews_data = pd.read_csv('data/USNews_USUniversity_Rankings.csv')
    process_rank_below_zero(USNews_data)
    QS_data['normalizedName'] = QS_data['Name'].str.lower()
    QS_data['normalizedName'] = QS_data['normalizedName'].apply(normalize_name)
    QS_data.rename(columns={'Rank':'QS_rank'}, inplace=True)
    USNews_data['normalizedName'] = USNews_data['Name'].str.lower()
    USNews_data['normalizedName'] = USNews_data['normalizedName'].apply(normalize_name)
    USNews_data.rename(columns={'Rank':'USNews_US_Rank'}, inplace=True)
    Merged_data = merge_dataframes(QS_data, USNews_data)

    # Loading data from US News Global University Rankings json file
    with open("data/usnews_detailed_data.json", "r", encoding="utf-8") as f:
        content = f.read()
        # print("Length:", len(content))
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
    USNews_global_data = pd.DataFrame(data)
    process_rank_below_zero(USNews_global_data)
    USNews_global_data.rename(columns={'Rank':'USNews_global_rank'}, inplace=True)
    USNews_global_data['normalizedName'] = USNews_global_data['Name'].str.lower()
    USNews_global_data['normalizedName'] = USNews_global_data['normalizedName'].apply(normalize_name)
    Merged_data = merge_dataframes(Merged_data, USNews_global_data)
    return Merged_data

def write_data_to_json():
    with open('data/final_json.json','w') as file:
        

def write_data_to_csv():
    with open('data/merged_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        data = load_data()
        writer.writerow(data.columns)
        for index, row in data.iterrows():
            writer.writerow(row)