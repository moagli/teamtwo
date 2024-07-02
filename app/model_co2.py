import psycopg2
import pandas as pd
from matplotlib import pyplot as plt
import io
import base64

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



def calc_co2():
    cur.execute("SELECT * FROM amex_raw")
    st_amex = cur.fetchall()
    columns = [column[0] for column in cur.description]
    # Create a Pandas DataFrame from the fetched data
    df_amex = pd.DataFrame(st_amex, columns=columns)

    cur.execute("SELECT * FROM starling")
    st_star = cur.fetchall()
    columns = [column[0] for column in cur.description]
    # Create a Pandas DataFrame from the fetched data
    df_star = pd.DataFrame(st_star, columns=columns)
    return pd.concat([df_star, df_amex], ignore_index=True)


def top10():
    df = calc_co2()
    df = df[df['eco_cat'].isin(["Grocery/Supermarket","Dining/Restaurants","Clothing/Retail","Travel","Entertainment/Recreation"])]


    top_10_a = df.sort_values('co2_est', ascending=False).head(10)
    return top_10_a[['date', 'counterparty', 'eco_cat', 'co2_est']]

def monthly_chart():
    df = calc_co2()
    df['month'] = pd.to_datetime(df['date']).dt.month

    # Create a bar chart with all 12 months
    month_totals = df.groupby('month')['co2_est'].sum().reindex(range(1, 13), fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    month_totals.astype(float).plot(kind='bar')

    ax.set_xlabel('Month')
    ax.set_ylabel('Total est_co2')
    ax.set_title('Monthly Total est_co2')
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    return plot_url



if __name__ == '__main__':
    monthly_chart()
    print()