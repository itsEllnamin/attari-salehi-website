from django.shortcuts import render, redirect
from django.views import View
from utils import page_path
# from apps.warehouses.models import Warehouse, WarehouseType
from .models import Payment
from apps.orders.models import OrderStatus
from apps.accounts.models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from django.conf import settings
import requests
import json


appname = 'payments'

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


class ZarinpalPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            amount = order.get_final_price()
            description = 'پرداخت از طریق درگاه زرین‌پال انجام شد'
            payment = Payment.objects.create(
                order = order,
                customer = Customer.objects.get(user=request.user),
                amount = amount,
                description = description
            )
            request.session['payment_session'] = {
                'order_id': order_id,
                'payment_id': payment.id
            }
            CallbackURL = 'http://127.0.0.1:8080/payments/verify_zarinpal_payment/'
            phone = request.user.mobile_number
            Email = request.user.email
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": amount*10,
                "Description": description,
                "Phone": phone,
                "Email": Email,
                "CallbackURL": CallbackURL,
            }
            data = json.dumps(data)
            
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
        
        except Order.DoesNotExist:
            redirect('orders:checkout', order_id)
        except Customer.DoesNotExist:
            redirect('orders:checkout', order_id)
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request, authority):
        order_id = request.session['payment_session']['order_id']
        payment_id = request.session['payment_session']['payment_id']
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(id=payment_id)
        amount = order.get_final_price()
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount*10,
        "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.is_finally = True
                order.order_status = OrderStatus.objects.get(id=1)
                order.save()
                payment.is_finally = True
                payment.status_code = response['Status']
                payment.ref_id = response['RefID']
                payment.save()
                # for item in order.order_details.all():
                #     Warehouse.objects.create(
                #         type = WarehouseType.objects.get(id=2),
                #         user_registered = request.user,
                #         product = item.product,
                #         qty = item.qty,
                #         price = item.price
                #     )
                
                return {'status': True, 'RefID': response['RefID']}
            else:
                payment.status_code = response['Status']
                payment.save()
                return {'status': False, 'code': str(response['Status'])}
        return response


def show_verification_message(request, message):
    return render(request, page_path(appname, 'verify_message'), {'message': message})