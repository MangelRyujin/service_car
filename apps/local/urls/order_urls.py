from django.urls import path
from apps.local.views.order_views import *

urlpatterns = [
    path('',order_view,name='order_view'),
    path('order_results_view',order_results_view,name='order_results_view'),
    path('order_create',order_create,name='order_create'),
    path('order_detail/<int:pk>/',order_detail,name='order_detail'),
    path('order_update/<int:pk>/',order_update,name='order_update'),
    path('update_order_extra_item_update/<int:pk>/',update_order_extra_item_update,name='update_order_extra_item_update'),
    
    path('update_order_item_create/<int:pk>/',update_order_item_create,name='update_order_item_create'),
    path('update_order_extra_item_create/<int:pk>/',update_order_extra_item_create,name='update_order_extra_item_create'),
    path('order_item_create/<int:pk>/',order_item_create,name='order_item_create'),
    path('order_extra_item_create/<int:pk>/',order_extra_item_create,name='order_extra_item_create'),
    
    path('order_delete/<int:pk>/',order_delete,name='order_delete'),
    path('update_order_item_delete/<int:pk>/',update_order_item_delete,name='update_order_item_delete'),
    path('order_item_delete/<int:pk>/',order_item_delete,name='order_item_delete'),
    path('order_extra_item_delete/<int:pk>/',order_extra_item_delete,name='order_extra_item_delete'),
    path('update_order_extra_item_delete/<int:pk>/',update_order_extra_item_delete,name='update_order_extra_item_delete'),
    
    path('order_discount/<int:pk>/',order_discount,name='order_discount'),
    path('order_sold/<int:pk>/',order_sold,name='order_sold')
    
    
]

