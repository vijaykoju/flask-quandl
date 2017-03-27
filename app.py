'''
App to plot quandl stock closing data of last month
'''
from __future__ import print_function

import flask
import requests
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import datetime

app = flask.Flask(__name__)

colors = {
	'Black': '#000000',
	'Red':   '#FF0000',
	'Green': '#00FF00',
	'Blue':  '#0000FF',
}

def getitem(obj, item, default):
	if item not in obj:
		return default
	else:
		return obj[item]

@app.route("/")
def plot_quandl():
	# Grab the inputs arguments from the URL
	args = flask.request.args
	
	# Get all the form arguments in the url with defaults
	color = getitem(args, 'color', 'Black')
	ticker = getitem(args, 'ticker', 'GOOG')
	
	today = datetime.date.today()
	last_month = today.month - 1

	if last_month < 10:
		sd = '0'+str(last_month)
		ed = '0'+str(today.month)
	else:
		sd = str(last_month)
		ed = str(today.month)

	start_date = str(today.year)+sd+'01'
	end_date= str(today.year)+ed+'01'
	
	req = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte='+start_date+'&date.lt='+end_date+'&ticker='+ticker+'&qopts.columns=date,close&api_key=your_quandl_api_key_here'
	r = requests.get(req)
	data = pd.DataFrame(np.array(r.json()['datatable']['data']))
	data[0] = pd.to_datetime(data[0])

	x = data[0]
	y = data[1]
	print(x)
	fig = figure(title=ticker+' closing stock of last month', x_axis_type='datetime')
	fig.line(x, y, color=colors[color], line_width=1)
	
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	
	script, div = components(fig)
	html = flask.render_template(
		'index.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
		color=color,
		ticker=ticker
	)
	return encode_utf8(html)

if __name__ == "__main__":
	app.run(port=33507)
