from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order', views.add_product_to_order, name='add_product_to_order'),
    path('request-payment/', views.request_payment, name='request_payment'),  # درخواست به سمت سرور زرین پال برای پرداخت
    path('verify-payment/', views.verify_payment, name='verify_payment'),  # نتیجه نهایی حالا جه پرداخت شده چه نشده
]
