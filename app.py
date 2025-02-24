from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/county_data', methods=['POST'])
def county_data():
    # Check content type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()

    # Check for teapot easter egg
    if data.get('coffee') == 'teapot':
        return '', 418

    # Validate required fields
    if 'zip' not in data or 'measure_name' not in data:
        return jsonify({"error": "Both zip and measure_name are required"}), 400

    zip_code = data['zip']
    measure_name = data['measure_name']

    # Validate zip code format
    if not (zip_code.isdigit() and len(zip_code) == 5):
        return jsonify({"error": "ZIP code must be 5 digits"}), 400

    # List of valid measure names
    valid_measures = {
        'Violent crime rate',
        'Unemployment',
        'Children in poverty',
        'Diabetic screening',
        'Mammography screening',
        'Preventable hospital stays',
        'Uninsured',
        'Sexually transmitted infections',
        'Physical inactivity',
        'Adult obesity',
        'Premature Death',
        'Daily fine particulate matter'
    }

    # Validate measure name
    if measure_name not in valid_measures:
        return jsonify({"error": "Invalid measure_name"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Join query to get county data based on zip code
        query = """
        SELECT ch.*
        FROM county_health_rankings ch
        JOIN zip_county zc ON ch.fipscode = zc.fipscode
        WHERE zc.zip = ? AND ch.measure_name = ?
        """
        
        cursor.execute(query, (zip_code, measure_name))
        results = cursor.fetchall()
        
        if not results:
            return jsonify({"error": "No data found for the given ZIP code and measure"}), 404

        # Convert results to list of dictionaries
        output = []
        for row in results:
            output.append({key: row[key] for key in row.keys()})

        conn.close()
        return jsonify(output)

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
