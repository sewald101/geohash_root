import json
import numpy as np
import pandas as pd
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .top_bygeo import trending_by_geo
from .models import Woeids
from .forms import SelectCountry


# Create your views here.
def index(request):
    countries = Woeids.objects.values('country').distinct().order_by('country')
    ww = trending_by_geo(woeid=1)
    form = SelectCountry()
    context = {'countries': countries, 'd': ww, 'form':form}
    return render(request, 'geohash/index.html', context)


def tophash_by_country(request):
    """Return results from country entered via the dropdown form on homepage.
    """
    print("LOG 2.0 - request object: {}".format(request))
    print("LOG 2.1 - request.GET object: {}".format(request.GET))
    print("LOG 2.2 - request.GET.country object: {}".format(request.GET['country']))
    country = request.GET['country']
    querySet = (
Woeids.objects.filter(name = country).filter(country = country).values('woeid')
        )
    print("LOG 2.3 - This is the country being passed to the Woeids query: {}"
          .format(country))
    print("LOG 2.4 - This is the querySet being passed to get 'woeid': {}"
          .format(querySet))
    woeid = querySet[0]['woeid']
    top_hashes = trending_by_geo(woeid=woeid)
    
    _NAMES = []
    q_set = (
        Woeids.objects.filter(country=country).values('name').order_by('name')
    )
    for d in q_set:
        for k, v in d.items():
           _NAMES.append((v,v))
    _NAMES.insert(0, ('', ''))
    
    if len(_NAMES) > 1: # Test if metros under countries; _NAMES will always
                        # include country name (hence, test > 1)
        print("LOG 2.5 - Metro Names: {}".format(_NAMES))
        class _SelectMetro(forms.Form):
            metro = forms.ChoiceField(widget=forms.Select, choices=_NAMES)
        form = _SelectMetro()
    else:
        form = None
    
    context = {'country': country, 'form': form, 'd': top_hashes}
    return render(request, "geohash/result.html", context)


def tophash_by_metro(request):
    """Return result from metro entered via dropdown from country results page.
    """
    metro = request.GET['metro']
    querySet = (
        Woeids.objects.filter(name = metro).values('woeid', 'country')
    )
    woeid = querySet[0]['woeid']
    print("LOG 3.1 - woeid: {}".format(woeid))
    country = querySet[0]['country']
    top_hashes = trending_by_geo(woeid=woeid)
    print("LOG 3.2 - top_hashes output: {}".format(top_hashes))
    context = {'name': metro, 'country': country, 'd': top_hashes}
    return render(request, "geohash/result.html", context)


def tophash_manual(request, name='', country=''):
    """ Return results from country and/or name parameters entered manually
    via the address bar of the browser with the '/m/' pattern. 
        E.g. localhost:8000/geohash/m/france/paris
    """
    print("LOG 1.0 - request object: {}".format(request))
    print("LOG 1.1 - request.GET object: {}".format(request.GET))
    country = country.title()
    name = name.title()
    if not country: # For worldwide
        querySet = (
        Woeids.objects.filter(name = name).values('woeid')
        )
    elif not name: # For countries at country grain
        querySet = (
Woeids.objects.filter(name = country).filter(country = country).values('woeid')
        )
    else: # For country, city
        querySet = (
        Woeids.objects.filter(name = name).filter(country = country).values('woeid')
        )
    print("LOG 1.2 - This is the country being passed to the Woeids query: {}"
          .format(country))
    print("LOG 1.3 - This is the querySet being passed to get 'woeid': {}"
          .format(querySet))
    woeid = querySet[0]['woeid']
    top_hashes = trending_by_geo(woeid=woeid)
    context = {'country': country, 'name': name, 'd': top_hashes}
    return render(request, "geohash/result.html", context)
