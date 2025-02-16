
from django.urls import path
from apps.local.views.reports_views import *

urlpatterns = [

    path('',report_order_view,name='report_order_view'),
    path('reports_order_table_results/',reports_order_table_results,name='reports_order_table_results'),
    path('reports_order_detail/<int:pk>/',reports_order_detail,name='reports_order_detail'),
    

    
]

