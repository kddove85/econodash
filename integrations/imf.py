import requests


us_only = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US'
multi = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US+CN+GB.'


def get_data(data_set, frequency, region, indicator):
    legends = []
    labels = []
    values = []
    entries = []
    url = f"http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/{data_set}/{frequency}.{region}.{indicator}"
    response = requests.get(url).json()
    series = response['CompactData']['DataSet']['Series']

    if isinstance(series, dict):
        print("Dictionary")
        ref_area = series['@REF_AREA']
        legends.append(ref_area)
        data = series['Obs']
        for entry in data:
            entries.append({'location': ref_area, 'time': entry['@TIME_PERIOD'], 'value': entry['@OBS_VALUE']})
            labels.append(entry['@TIME_PERIOD'])
            values.append(entry['@OBS_VALUE'])

    if isinstance(series, list):
        print("List")
        for location in series:
            ref_area = location['@REF_AREA']
            legends.append(ref_area)
            data = location['Obs']
            for entry in data:
                entries.append({'location': ref_area, 'time': entry['@TIME_PERIOD'], 'value': entry['@OBS_VALUE']})
                labels.append(entry['@TIME_PERIOD'])
                values.append(entry['@OBS_VALUE'])

    print(entries)
    print("Done")

    return legends, labels, values
