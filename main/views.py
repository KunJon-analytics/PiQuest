from django.http.response import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import json


# Create your views here.
cmc = CoinMarketCapAPI(settings.CMC_PRO_API_KEY)


class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = cmc.cryptocurrency_quotes_latest(
            symbol='BTC,ETH,BNB,DOGE,WAVES,NSBT,ADA')
        if not r.error:
            nested_dictionary = r.data
            context['crypto_context'] = nested_dictionary
        return context
