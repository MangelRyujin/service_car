from django.urls import path
from apps.local.views.local_views import *

urlpatterns = [
    path('',local_view,name='local_view'),
    path('local_table_results',local_table_results,name='local_table_results'),
    path('local_create',local_create,name='local_create'),
    path('local_update/<int:pk>/',local_update,name='local_update'),
    path('local_form_update/<int:pk>/',local_form_update,name='local_form_update'),
    path('local_delete/<int:pk>/',local_delete,name='local_delete'),
    
    
]

