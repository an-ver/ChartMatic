from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from flask import Flask, render_template, request
from charts.bar_chart import generate_bar_chart
from charts.line_chart import generate_line_chart
from charts.scatter_plot import generate_scatter_plot

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ROOT'
app.config['MYSQL_DB'] = 'my_dbms'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_countries')
def get_countries():
    cur = mysql.connection.cursor()
    cur.execute("SELECT `Display_Name` FROM `countries`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/get_indicators')
def get_indicators():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT `Indicators` FROM `Indicators`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/bar_chart')
def bar_chart():
    country = request.args.getlist('countries')
    indicator = request.args.getlist('indicators')
    aggregation = request.args.get('aggregation')
    start_year = request.args.get('startYear')
    end_year = request.args.get('endYear')
    print(start_year,end_year)
    if not country or not indicator or not aggregation:
        return jsonify({"error": "Select Country and Indicator parameters"}), 400
    chart = generate_bar_chart(country, indicator, aggregation, start_year, end_year)
    return chart

# Scatter plot can only parse 1 country and 2 indicators
@app.route('/scatter_plot')
def scatter_plot():
    country = request.args.get('countries')
    indicators = request.args.getlist('indicators')
    if not country or len(indicators) != 2:
        return jsonify({"error": "Select Country and exactly 2 Indicators parameters"}), 400
    chart = generate_scatter_plot(country, indicators)
    return chart

@app.route('/line_chart')
def line_chart():
    country = request.args.getlist('countries')
    indicator = request.args.getlist('indicators')
    aggregation = request.args.get('aggregation')
    start_year = request.args.get('startYear')
    end_year = request.args.get('endYear')
    print(start_year,end_year)
    if not country or not indicator or not aggregation:
        return jsonify({"error": "Select Country and Indicator parameters"}), 400
    chart = generate_line_chart(country, indicator, aggregation, start_year, end_year)
    return chart

if __name__ == '__main__':
    app.run(debug=True)