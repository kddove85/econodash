from flask import Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
from integrations import quandl
from integrations import imf
import json
import pandas as pd

bp = Blueprint('econodash', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    legends_a, labels_a, values_a, colors_a = imf .get_data('IFS', 'A', 'US', 'NGDP_XDC')
    legends, labels, values, colors = imf.get_data('IFS', 'A', 'US+CN+GB+JP+DE+SG+HK', 'NGDP_XDC')
    gdp_labels, gdp_values = quandl.get_gdp_values()
    # gdp_annual_increases = quandl.get_gdp_annual_increase()
    interest_labels, interest_rates = quandl.get_effective_interest_rates()
    # inflation_rates = quandl.get_inflation_data_points()
    unemployment_labels, unemployment_rates = quandl.get_unemployment_rates()
    bot_labels, bot_values = quandl.get_balance_of_trade()
    debt_to_gdp_labels, debt_to_gdp_values = quandl.get_government_debt_to_gdp()
    context = {'legends': legends, 'labels': labels, 'values': values, 'colors': colors,
               'legends_a': legends_a, 'labels_a': labels_a, 'values_a': values_a, 'colors_a': colors_a,
               'gdp_labels': gdp_labels,
               'gdp_values': gdp_values,
               # 'gdp_annual_increases': gdp_annual_increases,
               'interest_labels': interest_labels,
               'interest_rates': interest_rates,
               # 'inflation_rates': inflation_rates,
               'unemployment_labels': unemployment_labels,
               'unemployment_rates': unemployment_rates,
               'bot_labels': bot_labels,
               'bot_values': bot_values,
               'debt_to_gdp_labels': debt_to_gdp_labels,
               'debt_to_gdp_values': debt_to_gdp_values}
    return render_template('index.html', response_obj=context)


@bp.route('/bar')
def bar():
    maximum = 0
    labels = []
    values = []
    gdp_values = quandl.get_gdp_values()
    for item in gdp_values[::-1]:
        labels.append(item[0])
        values.append(item[1])
        if item[1] > maximum:
            maximum = item[1]
    bar_labels = labels
    bar_values = values
    return render_template('bar_chart.html', title='GDP Values', max=maximum, labels=bar_labels,
                           values=bar_values)


# @bp.route('/', methods=['GET', 'POST'])
# def index():
#     chart_list = []
#     df = quandl.get_gdp_values()
#     for item in df:
#         chart_data = {'Date': item[0].strip(), 'Value': item[1]}
#         chart_list.append(chart_data)
#     # chart_data = df.to_dict(orient='records')
#     chart_data = json.dumps(chart_list, indent=2)
#     data = {'chart_data': chart_data}
#     return render_template("index_chart.html", data=data)


@bp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
