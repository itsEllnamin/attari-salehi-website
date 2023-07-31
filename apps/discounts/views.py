from django.shortcuts import redirect
from apps.orders.models import Order
from .models import DiscountCode
from .forms import DiscountCodeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from django.contrib import messages


appname = 'discounts'

def get_discount_code_or_exception(discount_code):
    code = DiscountCode.objects.get(
        discount_code = discount_code,
        is_active = True,
        start_datetime__lte = datetime.now(),
        end_datetime__gte = datetime.now()
        )
    return code

def get_order_or_exception(order_id):
    order = Order.objects.get(id=order_id)
    return order


class ApplyDiscountCode(LoginRequiredMixin, View):
    def post(self, request, order_id):
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            discount_code = form.cleaned_data['discount_code']
            discount_percent = 0
            try:
                order = get_order_or_exception(order_id)
                discount = get_discount_code_or_exception(discount_code)
                discount_percent = discount.discount_percent
                order.discount_percent = discount_percent
                order.save()
                messages.success(request, 'کد تخفیف با موفقیت اعمال شد', 'success')
                return redirect('orders:checkout', order_id)

            except DiscountCode.DoesNotExist:
                order.discount_percent = discount_percent
                order.save()
                messages.error(request, 'کد وارد شده معتبر نیست', 'danger')
            except Order.DoesNotExist:
                messages.error(request, 'سفارش موجود نیست', 'danger')
            return redirect('orders:checkout', order_id)
                