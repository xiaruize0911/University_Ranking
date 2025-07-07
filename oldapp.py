from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import load_data, normalize_name
import pandas as pd
from pandas.api.types import is_number

import pandas as pd

def is_all_string_numbers_or_nan(series):
    s = series.dropna().astype(str)
    return s.str.replace('.', '', regex=False).str.isnumeric().all()



app = Flask(__name__)
CORS(app)
data = load_data()
data = data.sort_values(
    by=['QS_rank', 'USNews_global_rank'],
    ascending=[True, True],
    na_position='last'
).reset_index(drop=True)

@app.route('/api/universities', methods=['GET'])
def get_universities_list_simple():
    """
    Endpoint to get a simple list of universities with their names and rankings.
    """
    universities = data[['Name','QS_rank','USNews_global_rank']].to_dict('records')
    # print("Universities data loaded successfully.")
    return jsonify(universities)

@app.route('/api/university/<query>', methods=['GET'])
def search_university(query):
    query = normalize_name(query)  # Normalize the query for better matching
    # Find all matches containing the substring
    matches = data.loc[data['normalizedName'].str.contains(query, case=False, na=False)]
    # print(f"Found {len(matches)} matches for query '{query}'")
    if len(matches) == 0:
        return jsonify({'error': 'No matching universities found'}), 404
    if len(matches) > 100:
        matches = matches.head(100)
    matches = matches.to_json(orient='index')
    return jsonify(matches)

@app.route('/api/search', methods=['GET'])
def wide_search():
    currentAvailable = data.copy()
    if request.args.get('q') is not None:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify({'error': 'No search query provided'}), 400
        query = normalize_name(query)
        results = []

        for index, school in currentAvailable.iterrows():
            for field, value in school.items():
                if is_number(value) or value is None or query.isdigit():
                    continue
                # print(f"Checking {value} in {field} for query '{query}'")
                if query in normalize_name(value):
                    results.append(index)
                    break
        if not results:
            return jsonify({'error': 'No results found'}), 404
        currentAvailable = currentAvailable.loc[results]

    if request.args.get('sort') is not None:
        sort_by = request.args.get('sort', '')
        print(f"Sorting by: {sort_by}, on currentAvailable with columns: {currentAvailable[sort_by]}")

        if sort_by in currentAvailable.columns:
            if is_all_string_numbers_or_nan(currentAvailable[sort_by]):
                currentAvailable = currentAvailable.loc[currentAvailable[sort_by].notna()]
                currentAvailable[sort_by]= currentAvailable[sort_by].replace(',' , '', regex=False)
                currentAvailable[sort_by]=currentAvailable[sort_by].astype(int)
                currentAvailable = currentAvailable.sort_values(by=sort_by, ascending=True, na_position='last')
            else:
                currentAvailable = currentAvailable.sort_values(by=sort_by, ascending=True, na_position='last', key=lambda x: x.str.lower())
            currentAvailable = currentAvailable.sort_values(by=sort_by, ascending=True, na_position='last')
        else:
            return jsonify({'error': f'Invalid sort field: {sort_by}'}), 400
        
    if request.args.get('country') is not None:
        country = request.args.get('country', '').strip().lower()
        if 'Country' in currentAvailable.columns:
            currentAvailable = currentAvailable[currentAvailable['Country'].str.lower() == country]
        else:
            return jsonify({'error': 'Country filter not available'}), 400

    if len(currentAvailable) > 100:
        currentAvailable = currentAvailable[:100]
    res = currentAvailable.to_json(orient='index')

    # print(f"Found {len(res)} results for query '{query}'")
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)