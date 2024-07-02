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

# fig, ax = plt.subplots(figsize=(12, 6))
# calc_co().plot(kind='bar', ax=ax)
# ax.set_title('Monthly CO2 Emissions')
# ax.set_xlabel('Month')
# ax.set_ylabel('CO2 Emissions (kg)')

# plt.show()

import matplotlib.pyplot as plt
import numpy as np


def create_gradient_bar(dashed_line_position, solid_line_position):
    """
    Creates a red to green gradient bar with the given value and lines.

    Parameters:
    value (int): The value to be displayed on the bar.
    dashed_line_position (int): The position of the dashed line.
    solid_line_position (int): The position of the solid line.
    """
    # Create the x-axis values
    x = np.linspace(0, 150, 151)

    # Create the gradient colors
    colors = np.zeros((151, 3))
    colors[:, 0] = 1 - x / 150  # Red component decreases from 1 to 0
    colors[:, 1] = x / 150  # Green component increases from 0 to 1
    colors[:, 2] = 0  # Blue component is always 0

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 2))

    # Plot the gradient bar
    ax.bar(x, np.ones_like(x), color=colors, edgecolor='none')

    # Add the value text
    # ax.text(value, 1, f"{value}", ha='center', va='bottom', fontsize=12)

    # Add the dashed line
    ax.axvline(x=dashed_line_position, color='black', linestyle='--', linewidth=2)

    # Add the solid line
    ax.axvline(x=solid_line_position, color='black', linestyle='-', linewidth=2)

    # Set the axis limits and labels
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel('Value')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return fig


dashed_line_position = 38
solid_line_position = 68

fig = create_gradient_bar(dashed_line_position, solid_line_position)
plt.show()