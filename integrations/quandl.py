import requests
import os

dataset_fred = 'FRED'
dataset_rateinf = 'RATEINF'

base_url = 'https://www.quandl.com/api/v3/datasets'

# gdp value (annual growth % to be calculated)
# https://www.quandl.com/api/v3/datasets/FRED/GDP.json?api_key=w5XpMeDZ69Vm6xAsvjVF

# effective interest rate
# https://www.quandl.com/api/v3/datasets/FRED/FEDFUNDS.json?api_key=w5XpMeDZ69Vm6xAsvjVF

# inflation data points (annual inflation rate % to be calculated)
# https://www.quandl.com/api/v3/datasets/RATEINF/CPI_USA.json?api_key=w5XpMeDZ69Vm6xAsvjVF

# unemployment rate
# https://www.quandl.com/api/v3/datasets/FRED/UNRATE.json?api_key=w5XpMeDZ69Vm6xAsvjVF

# balance of trade
# https://www.quandl.com/api/v3/datasets/FRED/BOPGSTB.json?api_key=w5XpMeDZ69Vm6xAsvjVF

# Government debt to GDP ratio
# https://www.quandl.com/api/v3/datasets/FRED/GFDEGDQ188S.json?api_key=w5XpMeDZ69Vm6xAsvjVF


def get_gdp_values():
    print('get gdp values')
    maximum = float('-INF')
    values = []
    labels = []
    url = f"{base_url}/{dataset_fred}/GDP.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    # get first 50 entries
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        values.append(entry[1])
        labels.append(entry[0])
        if entry[1] > maximum:
            maximum = entry[1]
    return labels, values, maximum


def get_gdp_annual_increase():
    # annual increases must be calculated
    # first entry/last entry
    url = f"{base_url}/{dataset_fred}/GDP.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    return response['dataset']['data'][:50]


def get_effective_interest_rates():
    print('get effective interest rates')
    maximum = float('-INF')
    values = []
    labels = []
    url = f"{base_url}/{dataset_fred}/FEDFUNDS.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        values.append(entry[1])
        labels.append(entry[0])
        if entry[1] > maximum:
            maximum = entry[1]
    return labels, values, maximum


def get_inflation_data_points():
    # annual increases must be calculated
    # first entry/last entry
    maximum = float('-INF')
    url = f"{base_url}/{dataset_rateinf}/CPI_USA.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        if entry[1] > maximum:
            maximum = entry[1]
    return entries, maximum


def get_unemployment_rates():
    print('get unemployment rate')
    maximum = float('-INF')
    values = []
    labels = []
    url = f"{base_url}/{dataset_fred}/UNRATE.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        labels.append(entry[0])
        values.append(entry[1])
        if entry[1] > maximum:
            maximum = entry[1]
    return labels, values, maximum


def get_balance_of_trade():
    maximum = float('INF')
    values = []
    labels = []
    url = f"{base_url}/{dataset_fred}/BOPGSTB.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        values.append(entry[1])
        labels.append(entry[0])
        if entry[1] < maximum:
            maximum = entry[1]
    return labels, values, maximum


def get_government_debt_to_gdp():
    maximum = float('-INF')
    values = []
    labels = []
    url = f"{base_url}/{dataset_fred}/GFDEGDQ188S.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        labels.append(entry[0])
        values.append(entry[1])
        if entry[1] > maximum:
            maximum = entry[1]
    return labels, values, maximum
