from django import forms
from .models import Woeids


def tuplefy_countries():
    """Query Woeids model for sorted list of countries and reformat into list of tuples
    for consumption by SelectCountry form class.
    """
    q_set = Woeids.objects.values('country').distinct().order_by('country')
    COUNTRIES = []
    for d in q_set:
        for k, v in d.items():
            COUNTRIES.append((v,v))
    return COUNTRIES

class SelectCountry(forms.Form):
    country = forms.ChoiceField(widget=forms.Select, choices=tuplefy_countries())
