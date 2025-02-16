
from django.urls import path
from apps.local.views.reports_users_views import *

urlpatterns = [
    path('',report_order_users_view,name='report_order_users_view'),
    path('order_users_table_results/',order_users_table_results,name='order_users_table_results'),
]

