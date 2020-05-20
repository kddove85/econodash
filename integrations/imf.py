import requests
import colors
import countries
from datetime import datetime, date, timezone
from currency_converter import CurrencyConverter


# us_only = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US'
# multi = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US+CN+GB.'
c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
base_url = f"http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData"


def get_data(data_set, frequency, region, indicator, percent=False, second_series=None):
    legends = []
    labels = []
    values = []
    country_colors = []
    url = f"{base_url}/{data_set}/{frequency}.{region}.{indicator}"
    response = requests.get(url).json()
    series = response['CompactData']['DataSet']['Series']

    if isinstance(series, dict) and second_series is None:
        ref_area = series['@REF_AREA']
        country_colors.append(colors.colors[ref_area])
        legends.append(ref_area)
        if frequency == 'M':
            data = series['Obs'][-100:]
        else:
            data = series['Obs'][-50:]
        values_set = []
        for entry in data:
            labels.append(entry['@TIME_PERIOD'])
            values_set.append(entry['@OBS_VALUE'])
        values.append(values_set)

    if isinstance(series, list) or second_series is not None:
        if second_series is not None:
            returned_series = series
            series = [returned_series, second_series]
        date_range = get_range(series)
        for location in series:
            ref_area = location['@REF_AREA']
            legends.append(ref_area)
            country_colors.append(colors.colors[ref_area])
            data = location['Obs']
            values_set = []
            for entry in data:
                try:
                    new_time = datetime.strptime(entry['@TIME_PERIOD'], '%Y')
                    max_time = datetime.strptime(date_range['maximum'], '%Y')
                    min_time = datetime.strptime(date_range['minimum'], '%Y')
                except ValueError:
                    new_time = datetime.strptime(entry['@TIME_PERIOD'], '%Y-%m')
                    max_time = datetime.strptime(date_range['maximum'], '%Y-%m')
                    min_time = datetime.strptime(date_range['minimum'], '%Y-%m')
                if min_time <= new_time <= max_time:
                    if entry['@TIME_PERIOD'] not in labels:
                        labels.append(entry['@TIME_PERIOD'])
                    if ref_area != 'US' and ref_area != 'US2' and not percent:
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
    if len(series) > 2:
        final_date_range = {'maximum': float("Inf"), 'minimum': -float("Inf")}
    else:
        final_date_range = {'maximum': '2100-01', 'minimum': '1900-01'}
    for location in series:
        if len(series) > 2:
            date_range = {'maximum': -float("Inf"), 'minimum': float("Inf")}
            data = location['Obs'][-20:]
        else:
            date_range = {'maximum': '1900-01', 'minimum': '2100-01'}
            data = location['Obs']
        for item in data:
            if '-' in item['@TIME_PERIOD']:
                new_time = datetime.strptime(item['@TIME_PERIOD'], '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
                min_time = datetime.strptime(date_range['minimum'], '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
                max_time = datetime.strptime(date_range['maximum'], '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
                if new_time < min_time:
                    date_range['minimum'] = item['@TIME_PERIOD']
                if new_time > max_time:
                    date_range['maximum'] = item['@TIME_PERIOD']
            else:
                if float(item['@TIME_PERIOD']) < float(date_range['minimum']):
                    date_range['minimum'] = item['@TIME_PERIOD']
                if float(item['@TIME_PERIOD']) > float(date_range['maximum']):
                    date_range['maximum'] = item['@TIME_PERIOD']
        ranges.append(date_range)
    for item in ranges:
        if '-' in item['maximum'] or '-' in item['minimum']:
            min_time = datetime.strptime(item['minimum'], '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
            max_time = datetime.strptime(item['maximum'], '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
            final_min_time = datetime.strptime(final_date_range['minimum'],
                                               '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
            final_max_time = datetime.strptime(final_date_range['maximum'],
                                               '%Y-%m').replace(tzinfo=timezone.utc).timestamp()
            if max_time < final_max_time:
                final_date_range['maximum'] = item['maximum']
            if min_time > final_min_time:
                final_date_range['minimum'] = item['minimum']
        else:
            if float(item['maximum']) < float(final_date_range['maximum']):
                final_date_range['maximum'] = item['maximum']
            if float(item['minimum']) > float(final_date_range['minimum']):
                final_date_range['minimum'] = item['minimum']
    return final_date_range
