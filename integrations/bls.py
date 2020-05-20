import requests
import json
import datetime
import colors

url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'


def get_data_dictionary(series_id):
    dictionary = {'@REF_AREA': 'US2', 'Obs': []}
    previous = {
        'M01': None,
        'M02': None,
        'M03': None,
        'M04': None,
        'M05': None,
        'M06': None,
        'M07': None,
        'M08': None,
        'M09': None,
        'M10': None,
        'M11': None,
        'M12': None,
    }
    legends = ['US']
    country_colors = []
    for item in legends:
        country_colors.append(colors.colors[item])
    start_year, end_year = get_years()
    headers = {'Content-type': 'application/json'}
    data = json.dumps(
        {"seriesid": [series_id], "startyear": start_year, "endyear": end_year, "annualaverage": True,
         "registrationkey": "a356c4a051584b0dad37f2012a5d7f75"})
    p = requests.post(url, data=data, headers=headers)
    json_data = json.loads(p.text)
    result_data = json_data['Results']['series'][0]['data']
    for item in reversed(result_data):
        if previous[item['period']] is None:
            previous[item['period']] = item['value']
        else:
            label = f"{item['year']}-{item['period'][1:]}"
            new = (float(item['value']) - float(previous[item['period']])) / float(previous[item['period']])
            dictionary['Obs'].append({'@TIME_PERIOD': label, '@OBS_VALUE': new})
            previous[item['period']] = item['value']
    return dictionary


def get_data_month_over_month(series_id):
    previous = {
        'M01': None,
        'M02': None,
        'M03': None,
        'M04': None,
        'M05': None,
        'M06': None,
        'M07': None,
        'M08': None,
        'M09': None,
        'M10': None,
        'M11': None,
        'M12': None,
    }
    legends = ['US']
    labels = []
    values = []
    country_colors = []
    for item in legends:
        country_colors.append(colors.colors[item])
    start_year, end_year = get_years()
    headers = {'Content-type': 'application/json'}
    data = json.dumps(
        {"seriesid": [series_id], "startyear": start_year, "endyear": end_year, "annualaverage": True,
         "registrationkey": "a356c4a051584b0dad37f2012a5d7f75"})
    p = requests.post(url, data=data, headers=headers)
    json_data = json.loads(p.text)
    result_data = json_data['Results']['series'][0]['data']
    value_set = []
    for item in reversed(result_data):
        if previous[item['period']] is None:
            previous[item['period']] = item['value']
        else:
            labels.append(f"{item['year']}-{item['period'][1:]}")
            new = (float(item['value']) - float(previous[item['period']])) / float(previous[item['period']])
            value_set.append(new)
            previous[item['period']] = item['value']
    values.append(value_set)
    return legends, labels, values, country_colors


def get_data(series_id):
    legends = ['US']
    labels = []
    values = []
    country_colors = []
    for item in legends:
        country_colors.append(colors.colors[item])
    start_year, end_year = get_years()
    headers = {'Content-type': 'application/json'}
    data = json.dumps(
        {"seriesid": [series_id], "startyear": start_year, "endyear": end_year, "annualaverage": True,
         "registrationkey": "a356c4a051584b0dad37f2012a5d7f75"})
    p = requests.post(url, data=data, headers=headers)
    json_data = json.loads(p.text)
    result_data = json_data['Results']['series'][0]['data']
    value_set = []
    for item in reversed(result_data):
        # if previous[item['period']] is None:
        #     previous[item['period']] = item['value']
        # else:
        labels.append(f"{item['year']}-{item['period'][1:]}")
        # new = (float(item['value']) - float(previous[item['period']])) / float(previous[item['period']])
        value_set.append(item['value'])
        # previous[item['period']] = item['value']
    values.append(value_set)
    return legends, labels, values, country_colors


def get_years():
    end_year = datetime.datetime.now().year
    start_year = int(end_year) - 5
    start_year = str(start_year)
    return start_year, end_year
