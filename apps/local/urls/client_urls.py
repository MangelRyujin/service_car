
from django.urls import path
from apps.local.views.client_views import *

urlpatterns = [
    path('client_create/',client_create,name='client_create'),
    path('client_table_results/',client_table_results,name='client_table_results'),
    path('',client_view,name='client_view'),
    path('client_update/<int:pk>/',client_update,name='client_update'),
    
]

