from flask import Flask, request, render_template
import psycopg2
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from connections.startling_bank import calc_co

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
        co2_emissions NUMERIC(10,2)
    )
""")
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        # Get the form data
        merchant = request.form['merchant']
        amount = request.form['amount']
        co2_emissions = request.form['co2_emissions']

        # Insert the data into the database
        cur.execute("INSERT INTO credit_card_statements (merchant, amount, co2_emissions) VALUES (%s, %s, %s)", (merchant, amount, co2_emissions))
        conn.commit()

    # Fetch all the data from the database
    cur.execute("SELECT * FROM credit_card_statements")
    statements = cur.fetchall()

    return render_template('index.html', statements=statements)

@app.route('/')
def index():
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

    return render_template('index.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)