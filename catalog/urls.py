from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, my_contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('', contacts, name='contacts'),
    path('contacts/', my_contact, name='my_contact')
]
