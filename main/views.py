from django.http.response import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import json


# Create your views here.
cmc = CoinMarketCapAPI(settings.CMC_PRO_API_KEY)

def get_symbol_price(nested_dictionary, crypto):
    symbol_price = dict()
    for crypto in nested_dictionary:
        symbol = nested_dictionary[crypto]['symbol']
        price = nested_dictionary[crypto]['quote']['USD']['price']
        symbol_price[crypto] = {price, symbol}
    return symbol_price

def get_crypto_context(list):
    context_data = dict()
    for coin in list:
        context_data = get_symbol_price(nested_dictionary, coin)
    return context_data

class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = cmc.cryptocurrency_quotes_latest(symbol='BTC,ETH,BNB,DOGE,WAVES')
        nested_dictionary = r.data
        context['crypto_context'] = nested_dictionary
        return context



# def get_all_values(nested_dictionary):
#     for key, value in nested_dictionary.items():
#         if type(value) is dict:
#             get_all_values(value)
#         else:
#             print(key, ":", value)