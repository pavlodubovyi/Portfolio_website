from django.urls import path
from .views import NeedfulThingsView, CurrencyConverterView, RandomFactView

urlpatterns = [
    path('', NeedfulThingsView.as_view(), name='needful_things'),
    path('currency/', CurrencyConverterView.as_view(), name='currency_converter'),
    path('random_fact/', RandomFactView.as_view(), name='random_fact'),
]
