from django.urls import path
from .views import NeedfulThingsView

urlpatterns = [
    path('', NeedfulThingsView.as_view(), name='needful_things'),
]
