from flask import Flask, render_template
import datetime

application = Flask(__name__)
application.secret_key = 'cC1YCIaefjaelDNE2pgNEo2'


@application.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

application.jinja_env.filters['datetimefilter'] = datetimefilter


@application.route("/")
def home():
    return render_template('template.html')


# @application.route('/overview')
# def overview():
#     return render_template('template.html')


@application.route("/map")
def visualization():
    return render_template('template2.html')

if __name__ == '__main__':
    application.run(debug=True)
