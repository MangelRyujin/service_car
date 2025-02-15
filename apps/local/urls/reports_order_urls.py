
from django.urls import path
from apps.local.views.reports_views import *

urlpatterns = [

    path('',report_order_view,name='report_order_view'),
    path('order_table_results/',order_table_results,name='order_table_results'),
    path('order_detail/<int:pk>/',order_detail,name='order_detail'),
    

    
]

