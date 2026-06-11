from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search_customer, name='search'),
    path('history/', views.payment_history, name='history'),
    path('unpaid/', views.unpaid_customers, name='unpaid'),
    path(
        'mark-paid/<int:payment_id>/',
        views.mark_paid,
        name='mark_paid'
    ),
    path('customers/', views.customers, name='customers'),
    path('customer/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customer/delete/<int:id>/', views.delete_customer, name='delete_customer'),
]