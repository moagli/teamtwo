from flask import Flask, render_template, request, redirect, url_for
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
    password=DB_PASSWORD,
)

# Create a cursor object
cur = conn.cursor()

# Create the credit card statement table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS credit_card_statements (
        id SERIAL PRIMARY KEY,
        merchant TEXT,
        amount NUMERIC(10,2),
        est_co2_emissions NUMERIC(10,2),
        top_up_co2 NUMERIC(10,2)
    )
"""
)
conn.commit()

## top up table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS credit_card_statements (
        id SERIAL PRIMARY KEY,
        merchant TEXT,
        item NUMERIC(10,2),
        amount NUMERIC(10,2),
        est_co2_emissions NUMERIC(10,2),
        top_up_co2 NUMERIC(10,2)
    )
"""
)
conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files["file"]
        if file:
            # Read the CSV file
            spending_data = pd.read_csv(file)

            # Map the categories to the ones used in the carbon footprint values
            # spending_data["Category"] = spending_data["Category"].map(category_mapping)
            #
            # # Calculate the carbon footprint for each transaction
            # spending_data["Carbon Footprint"] = spending_data.apply(
            #     lambda row: (category_carbon_values.get(row["Category"], (0, 0))[0] +
            #                  category_carbon_values.get(row["Category"], (0, 0))[1]) / 2 * (row["Amount"] / 100),
            #     axis=1
            # )
            #
            # # Insert the data into the SQLite database
            # for _, row in spending_data.iterrows():
            #     c.execute("INSERT INTO spending (Date, Category, Amount, 'Carbon Footprint') VALUES (?, ?, ?, ?)",
            #               (row['Date'], row['Category'], row['Amount'], row['Carbon Footprint']))
            # conn.commit()

            # Redirect to the index page
            return redirect(url_for("index"))

        # Get the form data
        # merchant = request.form['merchant']
        # amount = request.form['amount']
        # co2_emissions = request.form['co2_emissions']
        #
        # # Insert the data into the database
        # cur.execute("INSERT INTO credit_card_statements (merchant, amount, co2_emissions) VALUES (%s, %s, %s)", (merchant, amount, co2_emissions))
        # conn.commit()

    # Fetch all the data from the database
    cur.execute("SELECT * FROM credit_card_statements")
    statements = cur.fetchall()

    co2_value_1 = 40
    co2_value_2 = 38
    return render_template(
        "index.html", co2_value_1=co2_value_1, co2_value_2=co2_value_2
    )
    # return render_template('index.html', statements=statements)


@app.route("/detail")
def detail():
    # Generate the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    calc_co().plot(kind="bar", ax=ax)
    ax.set_title("Monthly CO2 Emissions")
    ax.set_xlabel("Month")
    ax.set_ylabel("CO2 Emissions (kg)")

    # Convert the plot to a base64-encoded image
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode("utf8")

    return render_template("detail.html", plot_url=plot_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
