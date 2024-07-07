from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Load the updated RFM table csv file
rfm_table_path = 'updated_rfm_table.csv'
rfm_table = pd.read_csv(rfm_table_path, encoding='ISO-8859-1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_page')
def search_page():
    return render_template('search.html')

@app.route('/prediction_page')
def prediction_page():
    return render_template('predict.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('searchQuery', '')
    promotion_filter = request.form.get('promotionFilter', '')
    update_filter = request.form.get('updateFilter', '')
    r_filter = request.form.get('rFilter', '')
    f_filter = request.form.get('fFilter', '')
    m_filter = request.form.get('mFilter', '')
    interest_filter = request.form.get('interestFilter', '')

    # Filter the DataFrame based on the search query and filters
    filtered_data = rfm_table

    if search_query:
        filtered_data = filtered_data[filtered_data['customer'].str.contains(search_query, case=False, na=False)]
    
    if promotion_filter:
        filtered_data = filtered_data[filtered_data['promotion_frequency'] == promotion_filter]

    if update_filter:
        filtered_data = filtered_data[filtered_data['update_frequency'] == int(update_filter)]
    
    if r_filter:
        filtered_data = filtered_data[filtered_data['R_Quartile'] == int(r_filter)]

    if f_filter:
        filtered_data = filtered_data[filtered_data['F_Quartile'] == int(f_filter)]

    if m_filter:
        filtered_data = filtered_data[filtered_data['M_Quartile'] == int(m_filter)]
    
    if interest_filter:
        filtered_data = filtered_data[filtered_data['product_interest'].str.contains(interest_filter, case=False, na=False)]

    return jsonify(filtered_data.to_dict(orient='records'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        recency = int(data.get('recency', 0))
        frequency = int(data.get('frequency', 0))
        monetary = float(data.get('monetary', 0))
        product_interest = data.get('productInterest', '')

        # Combine the new data with the existing data to compute quartiles
        new_entry = pd.DataFrame({
            'Recency': [recency],
            'Frequency': [frequency],
            'Monetary': [monetary]
        })

        combined_data = pd.concat([rfm_table[['Recency', 'Frequency', 'Monetary']], new_entry])

        # Calculate RFM Quartiles
        combined_data['R_Quartile'] = pd.qcut(combined_data['Recency'], 4, labels=[4, 3, 2, 1])
        combined_data['F_Quartile'] = pd.qcut(combined_data['Frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4])
        combined_data['M_Quartile'] = pd.qcut(combined_data['Monetary'].rank(method="first"), 4, labels=[1, 2, 3, 4])

        # Extract the quartiles for the new data
        r_quartile = combined_data.iloc[-1]['R_Quartile']
        f_quartile = combined_data.iloc[-1]['F_Quartile']
        m_quartile = combined_data.iloc[-1]['M_Quartile']

        rfm_class = f'{r_quartile}{f_quartile}{m_quartile}'

        # Determine promotion and update frequencies
        promotion_frequencies = {
            '111': 'Once everyday',
            '112': 'Once every 2 days',
            '113': 'Once every 3 days',
            '114': 'Once every week',
            '121': 'Once every week',
            '122': 'Once every 2 weeks',
            '123': 'Once every month',
            '124': 'Once every 2 months',
            # Add more mappings as needed
        }

        update_frequencies = {
            '111': 1,
            '112': 2,
            '113': 3,
            '114': 4,
            '121': 4,
            '122': 5,
            '123': 5,
            '124': 5,
            # Add more mappings as needed
        }

        promotion_frequency = promotion_frequencies.get(rfm_class, 'Once every 2 months')
        update_frequency = update_frequencies.get(rfm_class, 5)

        return jsonify({
            'R_Quartile': int(r_quartile),
            'F_Quartile': int(f_quartile),
            'M_Quartile': int(m_quartile),
            'RFMClass': rfm_class,
            'product_interest': product_interest,
            'promotion_frequency': promotion_frequency,
            'update_frequency': update_frequency
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Load the updated RFM table csv file
rfm_table_path = 'updated_rfm_table.csv'
rfm_table = pd.read_csv(rfm_table_path, encoding='ISO-8859-1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_page')
def search_page():
    return render_template('search.html')

@app.route('/prediction_page')
def prediction_page():
    return render_template('predict.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('searchQuery', '')
    promotion_filter = request.form.get('promotionFilter', '')
    update_filter = request.form.get('updateFilter', '')
    r_filter = request.form.get('rFilter', '')
    f_filter = request.form.get('fFilter', '')
    m_filter = request.form.get('mFilter', '')
    interest_filter = request.form.get('interestFilter', '')

    # Filter the DataFrame based on the search query and filters
    filtered_data = rfm_table

    if search_query:
        filtered_data = filtered_data[filtered_data['customer'].str.contains(search_query, case=False, na=False)]
    
    if promotion_filter:
        filtered_data = filtered_data[filtered_data['promotion_frequency'] == promotion_filter]

    if update_filter:
        filtered_data = filtered_data[filtered_data['update_frequency'] == int(update_filter)]
    
    if r_filter:
        filtered_data = filtered_data[filtered_data['R_Quartile'] == int(r_filter)]

    if f_filter:
        filtered_data = filtered_data[filtered_data['F_Quartile'] == int(f_filter)]

    if m_filter:
        filtered_data = filtered_data[filtered_data['M_Quartile'] == int(m_filter)]
    
    if interest_filter:
        filtered_data = filtered_data[filtered_data['product_interest'].str.contains(interest_filter, case=False, na=False)]

    return jsonify(filtered_data.to_dict(orient='records'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        recency = int(data.get('recency', 0))
        frequency = int(data.get('frequency', 0))
        monetary = float(data.get('monetary', 0))
        product_interest = data.get('productInterest', '')

        # Combine the new data with the existing data to compute quartiles
        new_entry = pd.DataFrame({
            'Recency': [recency],
            'Frequency': [frequency],
            'Monetary': [monetary]
        })

        combined_data = pd.concat([rfm_table[['Recency', 'Frequency', 'Monetary']], new_entry])

        # Calculate RFM Quartiles
        combined_data['R_Quartile'] = pd.qcut(combined_data['Recency'], 4, labels=[4, 3, 2, 1])
        combined_data['F_Quartile'] = pd.qcut(combined_data['Frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4])
        combined_data['M_Quartile'] = pd.qcut(combined_data['Monetary'].rank(method="first"), 4, labels=[1, 2, 3, 4])

        # Extract the quartiles for the new data
        r_quartile = combined_data.iloc[-1]['R_Quartile']
        f_quartile = combined_data.iloc[-1]['F_Quartile']
        m_quartile = combined_data.iloc[-1]['M_Quartile']

        rfm_class = f'{r_quartile}{f_quartile}{m_quartile}'

        # Determine promotion and update frequencies
        promotion_frequencies = {
            '111': 'Once everyday',
            '112': 'Once every 2 days',
            '113': 'Once every 3 days',
            '114': 'Once every week',
            '121': 'Once every week',
            '122': 'Once every 2 weeks',
            '123': 'Once every month',
            '124': 'Once every 2 months',
            # Add more mappings as needed
        }

        update_frequencies = {
            '111': 1,
            '112': 2,
            '113': 3,
            '114': 4,
            '121': 4,
            '122': 5,
            '123': 5,
            '124': 5,
            # Add more mappings as needed
        }

        promotion_frequency = promotion_frequencies.get(rfm_class, 'Once every 2 months')
        update_frequency = update_frequencies.get(rfm_class, 5)

        return jsonify({
            'R_Quartile': int(r_quartile),
            'F_Quartile': int(f_quartile),
            'M_Quartile': int(m_quartile),
            'RFMClass': rfm_class,
            'product_interest': product_interest,
            'promotion_frequency': promotion_frequency,
            'update_frequency': update_frequency
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
