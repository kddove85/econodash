import requests
import colors
import countries
from datetime import date
from currency_converter import CurrencyConverter


# us_only = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US'
# multi = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US+CN+GB.'
c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)


def get_data(data_set, frequency, region, indicator, percent=False):
    legends = []
    labels = []
    values = []
    country_colors = []
    url = f"http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/{data_set}/{frequency}.{region}.{indicator}"
    response = requests.get(url).json()
    series = response['CompactData']['DataSet']['Series']

    if isinstance(series, dict):
        ref_area = series['@REF_AREA']
        country_colors.append(colors.colors[ref_area])
        legends.append(ref_area)
        data = series['Obs'][-50:]
        values_set = []
        for entry in data:
            labels.append(entry['@TIME_PERIOD'])
            values_set.append(entry['@OBS_VALUE'])
        values.append(values_set)

    if isinstance(series, list):
        date_range = get_range(series)
        for location in series:
            ref_area = location['@REF_AREA']
            legends.append(ref_area)
            country_colors.append(colors.colors[ref_area])
            data = location['Obs']
            values_set = []
            for entry in data:
                if int(entry['@TIME_PERIOD']) in range(int(date_range['minimum'])-1, int(date_range['maximum'])+1):
                    if entry['@TIME_PERIOD'] not in labels:
                        labels.append(entry['@TIME_PERIOD'])
                    if ref_area != 'US' and not percent:
                        currency_code = countries.countries[ref_area]
                        number = float(entry['@OBS_VALUE'])
                        values_set.append(c.convert(number, currency_code, 'USD',
                                                    date=date(int(entry['@TIME_PERIOD']), 12, 31)))
                    else:
                        values_set.append(entry['@OBS_VALUE'])
            values.append(values_set)
        labels.sort()
        values = fill_zero(values)

    return legends, labels, values, country_colors


def fill_zero(value_list):
    max_len = 0
    for item in value_list:
        if len(item) > max_len:
            max_len = len(item)
    for item in value_list:
        while len(item) < max_len:
            item.insert(0, 0)
    return value_list


def get_range(series):
    ranges = []
    final_date_range = {'maximum': float("Inf"), 'minimum': -float("Inf")}
    for location in series:
        date_range = {'maximum': -float("Inf"), 'minimum': float("Inf")}
        data = location['Obs'][-20:]
        for item in data:
            if float(item['@TIME_PERIOD']) < float(date_range['minimum']):
                date_range['minimum'] = item['@TIME_PERIOD']
            if float(item['@TIME_PERIOD']) > float(date_range['maximum']):
                date_range['maximum'] = item['@TIME_PERIOD']
        ranges.append(date_range)
    for item in ranges:
        if float(item['maximum']) < float(final_date_range['maximum']):
            final_date_range['maximum'] = item['maximum']
        if float(item['minimum']) > float(final_date_range['minimum']):
            final_date_range['minimum'] = item['minimum']
    return final_date_range
