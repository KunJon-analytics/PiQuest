from django.http.response import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError


# Create your views here.
cmc = CoinMarketCapAPI(settings.CMC_PRO_API_KEY)


class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = cmc.cryptocurrency_quotes_latest(
            symbol='BTC,ETH,BNB,DOGE,WAVES,XRP,ADA,AXS')
        if not r.error:
            nested_dictionary = r.data
            context['crypto_context'] = nested_dictionary
        return context


class PrivacyPageView(TemplateView):
    template_name = 'main/privacy_policy.html'


def pi_validation(request):
    filename = "validation-key.txt"
    content = settings.PI_VALIDATION_KEY
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response
