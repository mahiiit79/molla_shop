from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect,reverse,render
import time
from product_module.models import Product
from .models import Order,OrderDetail
from django.conf import settings
import requests
import json

#'کدی که هنگام ثبت نام در سایت زرین پال بهمون میده'
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
#'از این سه تا ادرس زمانی استفاده میشه که میخوایم کاربر رو هدایت کنیم به صفحه پرداخت'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
#'مقدار مبلغ پرداختی'
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.

#'به زرین پال ارسال میشه برای اینکه مشخص کنه وقتی تراکنش کاربر تموم شد به کدوم ادرس فرستاده بشه و اطلاعات پرداختی رو به کی بده'
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request : HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1 :
        #count = 1
        return JsonResponse({
            'status': 'invalid_count',
            'text' : 'مقدار وارد شده معتبر نمی باشد.',
            'confirm_button_text':'مرسی از شما!'
        })


    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            # سبدخرید جاری کاربر
           # current_order = Order.objects.filter(is_paid=False,user_id=request.user.id).first()
            #'سبد خرید باز کاربر رو برمیگردونه اگه نداشته باشه میسازه دستورزیر'
            # current_order : Order = Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
            #created bool chon datsur get or create ye obj ba bool barmigardoone
            current_order,created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
           #دستور زیر برای اینکه که میاد چک میکنه ایا با این ایدی محصولی توی سبد خرید هست یا نه اگه بود ایف اجرا میشه اگه نبود الس
            current_order_detail =  current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None :
                #اگه ثبت شده بود محصولی با این ایدی میرم تعدادشو تغییر میدم
                current_order_detail.count += count
                current_order_detail.save()
                #اگه ثبت نشده بود میام میسازمش
            else:
                new_detail = OrderDetail(order_id=current_order.id,product_id=product_id,count=count)
                new_detail.save()
            # add product to order

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد.',
                'confirm_button_text': 'باشه ممنون!'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                 'text' : 'محصول مورد نظر یافت نشد!',
                 'confirm_button_text': 'مرسیییی'
            })



    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزوردن محصول به سبد خرید ابتدا می بایست وارد سایت شوید.',
            'confirm_button_text': 'ورود به سایت'
        })






@login_required
def request_payment(request : HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    #اگه سبدخرید کاربر خالی بود میگه کاربر رو بفرست به سبدخرید
    if total_price == 0 :
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        #"metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    #میاد دیتایی که از بالا گرفته رو به زرین پال ارسال میکنه
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    #حالا این ریکوئستی که ما ارسال کردیم یدونه آتراریتی برمیگردونه و ازش استفاده میکنه برای ری دایرکت کردن . درواقع میاد چک میکنه ببینه اگه کلک نزدی این پاییینی رو میفرسته به زیرن پال
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request : HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    #میگه اگه همه چیز اکی بود سبد خرید کاربر رو ببند و خرید رو نهایی کن.
    if request.GET.get('Status') == 'OK':
        #هدر رو میسازه
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        #دوباره همون دیتا رو ست میکنه
        #درواقع این کارو میکنه که هکر نیاد اطلاعات خرید رو تغییر بده
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10, # این مبلغی که اینجا ارسال میکنی باید با اوم مبلغ ریکوئست تابع بالا یکی باشه
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                #'current_order has to close'
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = req.json()['data']['ref_id']
                return render(request, 'order_module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'order_module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order_module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
