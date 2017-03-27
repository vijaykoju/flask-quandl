'''This example demonstrates embedding a standalone Bokeh document
into a simple Flask application, with a basic HTML web form.
To view the example, run:
    python simple.py
in this directory, and navigate to:
    http://localhost:5000
'''
from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import datetime
import quandl

quandl.ApiConfig.api_key = 'dvzXzx3iSej1nbvhG_HU'

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
def polynomial():
	""" Very simple embedding of a polynomial chart
	"""
	
	# Grab the inputs arguments from the URL
	args = flask.request.args
	
	# Get all the form arguments in the url with defaults
	color = getitem(args, 'color', 'Black')
	# _from = int(getitem(args, '_from', 0))
	# to = int(getitem(args, 'to', 10))
	ticker = getitem(args, 'ticker', 'GOOG')
	
	today = datetime.date.today()
	last_month = today.month - 1

	if last_month < 10:
		sd = '0'+str(last_month)
		ed = '0'+str(today.month)
	else:
		sd = str(last_month)
		ed = str(today.month)

	start_date = str(today.year)+'-'+sd+'-'+'01'
	end_date= str(today.year)+'-'+ed+'-'+'01'
	
	data = quandl.get_table('WIKI/PRICES', paginate=True, ticker=[ticker], date={'gte': start_date, 'lt': end_date}, qopts={'columns':['ticker', 'date', 'close']})

	# Create a polynomial line graph with those arguments
	# x = list(range(_from, to + 1))
	x = data['date']
	y = data['close']
	fig = figure(title=ticker+' closing stock of last month', x_axis_type='datetime')
	# fig.line(x, [i ** 2 for i in x], color=colors[color], line_width=2)
	fig.line(x, y, color=colors[color], line_width=1)
	
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	
	script, div = components(fig)
	html = flask.render_template(
		'embed.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
		color=color,
		# _from=_from,
		# to=to,
		ticker=ticker
	)
	return encode_utf8(html)

if __name__ == "__main__":
	print(__doc__)
	app.run(host='0.0.0.0')
