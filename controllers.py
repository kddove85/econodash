from flask import Blueprint, render_template, send_from_directory
from integrations import quandl
from integrations import imf

bp = Blueprint('econodash', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    domestic_gdp_legends, domestic_gdp_labels, domestic_gdp_values, domestic_gdp_colors = imf.get_data('IFS', 'A', 'US',
                                                                                                       'NGDP_XDC')
    comparative_gdp_legends, comparative_gdp_labels, comparative_gdp_values, comparative_gdp_colors = imf.get_data(
        'IFS', 'A', 'US+CN+GB+JP+DE+SG+HK', 'NGDP_XDC')
    domestic_gdp_percent_legends, domestic_gdp_percent_labels, domestic_gdp_percent_values, domestic_gdp_percent_colors = imf.get_data(
        'IFS', 'A', 'US', 'NGDP_D_PC_CP_A_PT')
    comparative_gdp_percent_legends, comparative_gdp_percent_labels, comparative_gdp_percent_values, comparative_gdp_percent_colors = imf.get_data(
        'IFS', 'A', 'US+CN+GB+JP+DE+SG+HK', 'NGDP_D_PC_CP_A_PT', percent=True)
    domestic_interest_rate_legends, domestic_interest_rate_labels, domestic_interest_rate_values, domestic_interest_rate_colors = imf.get_data(
        'IFS', 'A', 'US', 'FPOLM_PA')
    domestic_unemployment_rate_legends, domestic_unemployment_rate_labels, domestic_unemployment_rate_values, domestic_unemployment_rate_colors = imf.get_data(
        'IFS', 'A', 'US', 'LUR_PT')
    domestic_bot_legends, domestic_bot_labels, domestic_bot_values, domestic_bot_colors = imf.get_data('IFS', 'A', 'US',
                                                                                                       'NNXGS_XDC')
    comparative_bot_legends, comparative_bot_labels, comparative_bot_values, comparative_bot_colors = imf.get_data(
        'IFS', 'A', 'US+CN+GB+JP+DE+SG+HK', 'NNXGS_XDC')

    context = dict(domestic_gdp_legends=domestic_gdp_legends,
                   domestic_gdp_labels=domestic_gdp_labels,
                   domestic_gdp_values=domestic_gdp_values,
                   domestic_gdp_colors=domestic_gdp_colors,

                   comparative_gdp_legends=comparative_gdp_legends,
                   comparative_gdp_labels=comparative_gdp_labels,
                   comparative_gdp_values=comparative_gdp_values,
                   comparative_gdp_colors=comparative_gdp_colors,

                   domestic_gdp_percent_legends=domestic_gdp_percent_legends,
                   domestic_gdp_percent_labels=domestic_gdp_percent_labels,
                   domestic_gdp_percent_values=domestic_gdp_percent_values,
                   domestic_gdp_percent_colors=domestic_gdp_percent_colors,

                   comparative_gdp_percent_legends=comparative_gdp_percent_legends,
                   comparative_gdp_percent_labels=comparative_gdp_percent_labels,
                   comparative_gdp_percent_values=comparative_gdp_percent_values,
                   comparative_gdp_percent_colors=comparative_gdp_percent_colors,

                   domestic_interest_rate_legends=domestic_interest_rate_legends,
                   domestic_interest_rate_labels=domestic_interest_rate_labels,
                   domestic_interest_rate_values=domestic_interest_rate_values,
                   domestic_interest_rate_colors=domestic_interest_rate_colors,

                   domestic_unemployment_rate_legends=domestic_unemployment_rate_legends,
                   domestic_unemployment_rate_labels=domestic_unemployment_rate_labels,
                   domestic_unemployment_rate_values=domestic_unemployment_rate_values,
                   domestic_unemployment_rate_colors=domestic_unemployment_rate_colors,

                   domestic_bot_legends=domestic_bot_legends,
                   domestic_bot_labels=domestic_bot_labels,
                   domestic_bot_values=domestic_bot_values,
                   domestic_bot_colors=domestic_bot_colors,

                   comparative_bot_legends=comparative_bot_legends,
                   comparative_bot_labels=comparative_bot_labels,
                   comparative_bot_values=comparative_bot_values,
                   comparative_bot_colors=comparative_bot_colors
                   )

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
