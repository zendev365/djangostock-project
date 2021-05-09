from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


# HOME PAGE
def home(request):
	import requests
	import json

	# token=pk_727722b3049e4111a3be8188ef44027a
	api_token = "pk_727722b3049e4111a3be8188ef44027a"

	# return render(request, 'home.html', {})
	# return render(request, 'home.html', {'api':api})
	if request.method == 'POST':
		ticker = request.POST['ticker_symbol']

		# ticker = "aapl"
		api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + ticker + '/quote?token=' + api_token)

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "API Request Error"
		return render(request, 'home.html', {'api':api})
	else:
		# use default ticker
		api_request = requests.get('https://cloud.iexapis.com/stable/stock/vt/quote?token=' + api_token)
		# api_request = requests.get('https://cloud.iexapis.com/stable/stock/aieq/quote?token=' + api_token)
		# api_request = requests.get('https://cloud.iexapis.com/stable/stock/spy/quote?token=' + api_token)

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "API Request Error"

		return render(request, 'home.html', {'api':api})

# ABOUT PAGE
def about(request):
	return render(request, 'about.html', {})

# ADD STOCK PAGE (original)
# def add_stock(request):
# 	if request.method == 'POST':
# 		form = StockForm(request.POST or None)
#
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, ("Stock ticker has been added."))
# 			return redirect('add_stock')
#
# 	else:
# 		add_stock = Stock.objects.all()
# 		return render(request, 'add_stock.html', {'add_stock':add_stock})

# CONNECTING TO API SECTION BEGIN
def add_stock(request):
	import requests
	import json
	api_token = "pk_727722b3049e4111a3be8188ef44027a"

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock ticker has been added."))
			return redirect('add_stock')

	else:
		add_stock = Stock.objects.all()
		output = []

		for ticker_item in add_stock:
			api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + str(ticker_item) + '/quote?token=' + api_token)

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "API Request Error"

		return render(request, 'add_stock.html', {'add_stock':add_stock, 'output':output})

# CONNECTING TO API SECTION END

# DELETE STOCK SECTION BEGIN

def delete_stock(request):
	add_stock = Stock.objects.all()
	return render(request, 'delete_stock.html', {'add_stock':add_stock})

# DELETE STOCK SECTION END



# DELETE FUNCTION
def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Ticker has been deleted."))
	return redirect(delete_stock)
