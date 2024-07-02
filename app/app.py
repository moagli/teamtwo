from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from connections.amex import amex
from connections.startling_bank import star

import psycopg2
from psycopg2 import extras

from model_co2 import top10

app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "myapp"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create a cursor object
cur = conn.cursor()

# Create the credit card statement table
cur.execute("""
    CREATE TABLE IF NOT EXISTS credit_card_statements (
        id SERIAL PRIMARY KEY,
        merchant TEXT,
        amount NUMERIC(10,2),
        est_co2_emissions NUMERIC(10,2),
        top_up_co2 NUMERIC(10,2)
    )
""")
conn.commit()

## top up table
cur.execute("""
    CREATE TABLE IF NOT EXISTS credit_card_statements (
        id SERIAL PRIMARY KEY,
        merchant TEXT,
        item NUMERIC(10,2),
        amount NUMERIC(10,2),
        est_co2_emissions NUMERIC(10,2),
        top_up_co2 NUMERIC(10,2)
    )
""")
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Fetch all the data from the database
    statements = top10()
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file:
            # Read the CSV file
            spending_data = pd.read_csv(file)

            if "Notes" not in spending_data.columns:
                file_parser = amex(spending_data)
            else:
                file_parser = star(spending_data)

            cur.execute(file_parser.table_def())
            conn.commit()

            column_names = ', '.join(file_parser.file.columns)

            # Create a SQL INSERT statement
            sql = f"INSERT INTO {file_parser.tbl_nm} ({column_names}) VALUES %s"

            # Convert the DataFrame to a list of tuples
            values = [tuple(x) for x in file_parser.file.to_numpy()]

            # Use the execute_values function to insert the data
            cur.execute("BEGIN")
            psycopg2.extras.execute_values(cur, sql, values, template=None, page_size=100)
            cur.execute("COMMIT")

            # Redirect to the index page
            return redirect(url_for('index'), statements=statements)

    # return render_template('index.html')
    return render_template('index.html', statements=statements)

@app.route('/detail')
def detail():
    # Generate the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    calc_co().plot(kind='bar', ax=ax)
    ax.set_title('Monthly CO2 Emissions')
    ax.set_xlabel('Month')
    ax.set_ylabel('CO2 Emissions (kg)')

    # Convert the plot to a base64-encoded image
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('detail.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)