import pandas as pd
import csv

def load_data():
    QS_data = pd.read_csv('data/2026_QS_World_University_Rankings_1.0.csv')
    USNews_data = pd.read_csv('data/USNews_USUniversity_Rankings.csv')
    QS_data['Name'] = QS_data['Name'].str.lower()
    USNews_data['Name'] = USNews_data['Name'].str.lower()
    Merged_data = pd.merge(QS_data, USNews_data, on='Name', how='outer')
    return Merged_data

with open('data/merged_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    data = load_data()
    writer.writerow(data.columns)
    for index, row in data.iterrows():
        writer.writerow(row)

print("Data loaded successfully.")