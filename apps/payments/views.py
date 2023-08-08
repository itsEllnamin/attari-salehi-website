from django.shortcuts import render, redirect
from django.views import View
from utils import page_path
from apps.warehouses.models import Transaction, TransactionType
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
            CallbackURL = 'http://127.0.0.1:8000/payments/verify_zarinpal_payment/'
            phone = request.user.mobile_number
            Email = request.user.email
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": amount,
                "Description": description,
                "Phone": phone,
                "Email": Email,
                "CallbackURL": CallbackURL,
            }
            data = json.dumps(data)

            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    url = f"{ZP_API_STARTPAY}{response['Authority']}"
                    return redirect(url)
                else:
                    payment.status_code = response['Status']
                    payment.save()
                    return redirect('payments:show_verification_message', f'خطا در انتقال به درگاه، کد خطا {response["Status"]}')
            return redirect('payments:show_verification_message', f'خطا در درخواست، کد خطا {response.status_code}')

        except Order.DoesNotExist:
            redirect('orders:checkout', order_id)
        except Customer.DoesNotExist:
            redirect('orders:checkout', order_id)
        except requests.exceptions.Timeout as e:
            return redirect('payments:show_verification_message', f'خطا {e}')
        except requests.exceptions.ConnectionError as e:
            return redirect('payments:show_verification_message', f'خطا {e}')


class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        status = request.GET.get('Status')
        if status == 'OK':
            session = request.session
            payment_session = session.get('payment_session')
            shop_cart = session.pop('shop_cart', None)
            order_id = payment_session['order_id']
            order = Order.objects.get(id=order_id)
            amount = order.get_final_price()
            authority = request.GET.get('Authority')
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": amount,
                "Authority": authority,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    payment_id = payment_session['payment_id']
                    payment = Payment.objects.get(id=payment_id)

                    order.is_finally = True
                    order.order_status = OrderStatus.objects.get(id=1)
                    order.save()
                    payment.is_finally = True
                    payment.status_code = response['Status']
                    payment.ref_id = response['RefID']
                    payment.save()
                    for item in order.order_details.all():
                        Transaction.objects.create(
                            type = TransactionType.objects.get(id=2),
                            user_registered = request.user,
                            product = item.product,
                            qty = item.qty,
                            price = item.price
                        )
                    return redirect('payments:show_verification_message', f'پرداخت با موفقیت انجام شد، کد رهگیری شما {response["RefID"]}')
                elif response['Status'] == 101:
                    return redirect('payments:show_verification_message', f'پرداخت قبلا انجام شده، کد رهگیری شما {response["RefID"]}')

                payment.status_code = response['Status']
                payment.save()
                return redirect('payments:show_verification_message', f'خطا در فرآیند پرداخت، کد خطا {response["Status"]}')

            return redirect('payments:show_verification_message', f'خطا در درخواست، کد خطا {response.status_code}')

        return redirect('payments:show_verification_message', f'پرداخت لغو شد.')


def show_verification_message(request, message):
    return render(request, page_path(appname, 'verify_message'), {'message': message})