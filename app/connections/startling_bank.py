import pandas as pd



# Define the carbon footprint values per spending category
category_mapping = {
    'GROCERIES': 'Grocery/Supermarket',
    'ENTERTAINMENT': 'Entertainment/Recreation',
    'EATING_OUT': 'Dining/Restaurants',
    'BILLS_AND_SERVICES': 'Utilities',
    'HOME': 'Utilities',
    'TRANSPORT': 'Travel',
    'HOLIDAYS': 'Travel',
    'SHOPPING': 'Clothing/Retail',
    'CLOTHES': 'Clothing/Retail',
    'INCOME': 'General',
    'PAYMENTS': 'General',
    'GENERAL': 'General',
    'EXPENSES': 'General',
    'LIFESTYLE': 'General',
    'DIY': 'General',
    'CHILDREN': 'General',
    'NONE': 'General',
    'CASH': 'General'
}

# Define the carbon footprint values per spending category
category_carbon_values = {
    "Grocery/Supermarket": (0.5, 1.5),
    "Dining/Restaurants": (1.0, 2.5),
    "Clothing/Retail": (2.0, 5.0),
    "Travel": (5.0, 15.0),
    "Entertainment/Recreation": (1.0, 3.0),
    "Utilities": (2.0, 5.0),
    "General": (1.0, 3.0)
}


def calc_co():
    # Read the credit card spending data from a CSV file
    spending_data = pd.read_csv("/Users/ben/PycharmProjects/teamtwo/app/data/example_bank.csv")

    spending_data['Category'] = spending_data['Spending Category'].map(category_mapping)
    # Calculate the carbon footprint for each transaction
    spending_data["Carbon Footprint"] = spending_data.apply(
        lambda row: (category_carbon_values.get(row["Category"], (0, 0))[0] + category_carbon_values.get(row["Category"], (0, 0))[1]) / 2 * (row["Amount (GBP)"] / 100),
        axis=1
    ).abs()

    return spending_data


import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
calc_co().plot(kind='bar', ax=ax)
ax.set_title('Monthly CO2 Emissions')
ax.set_xlabel('Month')
ax.set_ylabel('CO2 Emissions (kg)')
plt.show()