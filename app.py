from flask import Flask, render_template, request, redirect
import datetime
import quandl
from bokeh.charts import Scatter, output_file

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  today = datetime.date.today()
  last_month = today.month - 1

  if last_month < 10:
    sd = '0'+str(last_month)
    ed = '0'+str(today.month)
  else:
    sd = str(last_month)
    ed = str(today.month)

  start_date = str(today.year)+'-'+sd+'-'+'01'
  end_date = str(today.year)+'-'+ed+'-'+'01'

  quandl.ApiConfig.api_key = 'dvzXzx3iSej1nbvhG_HU'

  ticker = 'AAPL'
  data = quandl.get_table('WIKI/PRICES', paginate=True, ticker=[ticker], date={'gte': start_date, 'lt': end_date}, qopts={'columns':['ticker', 'date', 'close']})

  p = Scatter(data, x="date", y="close", title="Closing stock", xlabel="Previous month date", ylabel="Closing stock")
  output_file("templates/Scatter_charts_closing_stock.html")
  return render_template('Scatter_charts_closing_stock.html')

if __name__ == '__main__':
  app.run(port=33507)
