from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Database connection and setup
conn = sqlite3.connect('accountancy_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS accountancy_data
             (id INTEGER PRIMARY KEY, item TEXT, amount FLOAT, co2_estimate FLOAT)''')
conn.commit()

# Function to estimate CO2 footprint based on item
def estimate_co2(item):
    # This is a simplified example, in practice you would need a more sophisticated model
    co2_factors = {
        'electricity': 0.5,
        'travel': 2.0,
        'office_supplies': 0.2,
        'equipment': 1.0
    }
    for key, value in co2_factors.items():
        if key in item.lower():
            return value
    return 0.5

@app.route('/data', methods=['POST'])
def upload_data():
    data = request.get_json()
    for item, amount in data.items():
        co2_estimate = estimate_co2(item)
        c.execute("INSERT INTO accountancy_data (item, amount, co2_estimate) VALUES (?, ?, ?)", (item, amount, co2_estimate))
    conn.commit()
    return jsonify({'message': 'Data uploaded successfully'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    c.execute("SELECT * FROM accountancy_data")
    data = c.fetchall()
    result = []
    for row in data:
        result.append({
            'id': row[0],
            'item': row[1],
            'amount': row[2],
            'co2_estimate': row[3]
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)