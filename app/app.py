from flask import Flask, request, render_template
import psycopg2

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
def index():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)