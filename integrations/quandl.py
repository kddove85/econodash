import requests
import os
import colors
import countries
from datetime import datetime, date, timezone
from currency_converter import CurrencyConverter
from frequencies import frequencies

dataset_fred = 'FRED'
dataset_rateinf = 'RATEINF'

base_url = 'https://www.quandl.com/api/v3/datasets'

# gdp value (annual growth % to be calculated)
# https://www.quandl.com/api/v3/datasets/FRED/GDP.json?api_key=

# effective interest rate
# https://www.quandl.com/api/v3/datasets/FRED/FEDFUNDS.json?api_key=

# inflation data points (annual inflation rate % to be calculated)
# https://www.quandl.com/api/v3/datasets/RATEINF/CPI_USA.json?api_key=

# unemployment rate
# https://www.quandl.com/api/v3/datasets/FRED/UNRATE.json?api_key=

# balance of trade
# https://www.quandl.com/api/v3/datasets/FRED/BOPGSTB.json?api_key=

# Government debt to GDP ratio
# https://www.quandl.com/api/v3/datasets/FRED/GFDEGDQ188S.json?api_key=


def get_gdp_values():
    return get_generic_request(dataset_fred, 'GDP')


def get_gdp_annual_increase():
    # annual increases must be calculated
    # first entry/last entry
    url = f"{base_url}/{dataset_fred}/GDP.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    return response['dataset']['data'][:50]


def get_effective_interest_rates():
    return get_generic_request(dataset_fred, 'FEDFUNDS')


def get_inflation_data_points():
    # annual increases must be calculated
    # first entry/last entry
    return get_generic_request(dataset_rateinf, 'CPI_USA')


def get_unemployment_rates():
    return get_generic_request(dataset_fred, 'UNRATE')


def get_balance_of_trade():
    return get_generic_request(dataset_fred, 'BOPGSTB')


def get_government_debt_to_gdp():
    return get_generic_request(dataset_fred, 'GFDEGDQ188S')


def get_generic_request(data_set, code):
    values = []
    labels = []
    url = f"{base_url}/{data_set}/{code}.json?api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    for entry in entries:
        labels.append(entry[0])
        values.append(entry[1])
    return labels, values


def get_data(data_set, frequency, region, indicator):
    legends = []
    labels = []
    values = []
    country_colors = []
    url = f"{base_url}/{data_set}/{indicator}.json?collapse={frequencies[frequency]}&api_key={os.getenv('api_key')}"
    response = requests.get(url).json()
    entries = response['dataset']['data'][:50][::-1]
    country_colors.append(colors.colors[region])
    legends.append(region)
    values_set = []
    for entry in entries:
        labels.append(entry[0])
        values_set.append(entry[1])
    values.append(values_set)

    return legends, labels, values, country_colors
