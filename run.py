from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route("/")
def home():
    return render_template('template.html')


# @app.route('/overview')
# def overview():
#     return render_template('template.html')


@app.route("/map")
def visualization():
    return render_template('template2.html')

if __name__ == '__main__':
    app.run(debug=True)
