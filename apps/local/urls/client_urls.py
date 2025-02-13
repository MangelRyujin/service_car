
from django.urls import path
from apps.local.views.client_views import *

urlpatterns = [
    path('client_create/',client_create,name='client_create'),
    
    
]

