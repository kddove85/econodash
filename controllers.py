from flask import Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
from integrations import quandl
import json
import pandas as pd

bp = Blueprint('econodash', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    gdp_labels, gdp_values, gdp_value_max = quandl.get_gdp_values()
    # gdp_annual_increases = quandl.get_gdp_annual_increase()
    interest_labels, interest_rates, interest_rates_max = quandl.get_effective_interest_rates()
    # inflation_rates = quandl.get_inflation_data_points()
    unemployment_labels, unemployment_rates, unemployment_rates_max = quandl.get_unemployment_rates()
    bot_labels, bot_values, bot_max = quandl.get_balance_of_trade()
    debt_to_gdp_labels, debt_to_gdp_values, debt_to_gdp_max = quandl.get_government_debt_to_gdp()
    context = {'gdp_labels': gdp_labels,
               'gdp_values': gdp_values,
               'gdp_values_max': gdp_value_max,
               # 'gdp_annual_increases': gdp_annual_increases,
               'interest_labels': interest_labels,
               'interest_rates': interest_rates,
               'interest_rates_max': interest_rates_max,
               # 'inflation_rates': inflation_rates,
               'unemployment_labels': unemployment_labels,
               'unemployment_rates': unemployment_rates,
               'unemployment_rates_max': unemployment_rates_max,
               'bot_labels': bot_labels,
               'bot_values': bot_values,
               'bot_max': bot_max,
               'debt_to_gdp_labels': debt_to_gdp_labels,
               'debt_to_gdp_values': debt_to_gdp_values,
               'debt_to_gdp_max': debt_to_gdp_max}
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