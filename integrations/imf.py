import requests
import colors


us_only = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US'
multi = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.US+CN+GB.'


def get_data(data_set, frequency, region, indicator):
    legends = []
    labels = []
    values = []
    url = f"http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/{data_set}/{frequency}.{region}.{indicator}"
    response = requests.get(url).json()
    series = response['CompactData']['DataSet']['Series']

    if isinstance(series, dict):
        print("Dictionary")
        ref_area = series['@REF_AREA']
        legends.append(ref_area)
        data = series['Obs']
        values_set = []
        for entry in data:
            labels.append(entry['@TIME_PERIOD'])
            values.append(entry['@OBS_VALUE'])
        values.append(values_set)

    if isinstance(series, list):
        print("List")
        for location in series:
            ref_area = location['@REF_AREA']
            legends.append(ref_area)
            data = location['Obs'][-50:]
            values_set = []
            for entry in data:
                if entry['@TIME_PERIOD'] not in labels:
                    labels.append(entry['@TIME_PERIOD'])
                values_set.append(entry['@OBS_VALUE'])
            values.append(values_set)

    print("Done")

    return legends, labels, values, colors.colors
