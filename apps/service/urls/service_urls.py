from django.urls import path
from apps.service.views.service_views import *

urlpatterns = [
    path('',service_view,name='service_view'),
    path('service_table_results',service_table_results,name='service_table_results'),
    path('service_create',service_create,name='service_create'),
    path('service_update/<int:pk>/',service_update,name='service_update'),
    path('service_form_update/<int:pk>/',service_form_update,name='service_form_update'),
    path('service_delete/<int:pk>/',service_delete,name='service_delete'),
    
    
]

