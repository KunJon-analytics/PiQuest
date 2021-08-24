from django.urls import path
from .views import ContactView, ClientContactView

app_name = 'contact'


urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    path('client/', ClientContactView.as_view(), name='client-contact'),
]