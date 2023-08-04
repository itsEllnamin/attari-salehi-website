from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import TemplateView, RedirectView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.products.models import Product
from apps.accounts.models import Customer
from apps.discounts.forms import DiscountCodeForm
from utils import page_path, partial_path, factor_details
from .shop_cart import ShopCart
from .models import PaymentType, Order, OrderDetail
from .forms import OrderForm
from django.contrib import messages
from django.urls import reverse_lazy



appname = "orders"
# =============================================== Shop Cart ==================================================
# ======================================= Partials ==========================================


class ShopCartDetail(TemplateView):
    template_name = partial_path(appname, "shop_cart_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_cart"] = shop_cart = ShopCart(self.request)
        context["total_price"] = total_price = shop_cart.calc_total_price()
        context["delivery_cost"], context["final_price"] = factor_details(total_price)
        return context


# ======================================= Pages  ==========================================


class ShopCartView(TemplateView):
    template_name = page_path(appname, "shop_cart")


# ======================================= Ajax ==========================================


def add_to_shop_cart(request):
    product_id = request.GET.get("product_id")
    qty = request.GET.get("qty")
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    shop_cart.add(product, qty)
    return HttpResponse()


def delete_from_shop_cart(request):
    product_id = request.GET.get("product_id")
    shop_cart = ShopCart(request)
    shop_cart.delete(product_id)
    return redirect("orders:shop_cart_detail")


def update_shop_cart(request):
    product_id_list = request.GET.getlist("product_id_list[]")
    qty_list = request.GET.getlist("qty_list[]")
    shop_cart = ShopCart(request)
    shop_cart.update(product_id_list, qty_list)
    return redirect("orders:shop_cart_detail")


def shop_cart_status(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)


# =============================================== Order ==================================================
# ======================================= Pages  ==========================================


class CreateOrderView(LoginRequiredMixin, RedirectView):
    permanent = True
    
    def get_redirect_url(self, *args, **kwargs):
        request = self.request
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        payment_type = get_object_or_404(PaymentType, id=1)
        order = Order.objects.create(customer=customer, payment_type=payment_type)
        self.url = reverse_lazy('orders:checkout', kwargs={'order_id': order.id})
        shop_cart = ShopCart(request)
        for item in shop_cart:
            OrderDetail.objects.create(
                order = order,
                product = item['product'],
                qty = item['qty'],
                price = item['price']
            )
        return super().get_redirect_url(*args, **kwargs)

class CheckoutOrderView(LoginRequiredMixin, View):
    template_name = page_path(appname, 'checkout')

    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        orders = customer.orders.all()
        order_id_list = [order.id  for order in orders]
        if  order_id == max(order_id_list) :
            shop_cart = ShopCart(request)
            order = get_object_or_404(Order, id=order_id, is_finally=False)
            total_price = shop_cart.calc_total_price()
            delivery_cost, final_price = factor_details(total_price, order.discount_percent)
            data = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'phone_number': customer.phone_number,
                'address': customer.address,
                'description': order.description,
                'payment_type': order.payment_type.id,
            }
            form = OrderForm(data)
            discount_code_form = DiscountCodeForm()
            context = {
                'shop_cart': shop_cart,
                'total_price': total_price,
                'delivery_cost': delivery_cost,
                # 'tax': tax,
                'order_id': order_id,
                'final_price': final_price,
                'form': form,
                'discount_code_form': discount_code_form,
            }
            return render(request, self.template_name, context)
        messages.error(request, 'سفارش یافت نشد', 'danger')
        return redirect('main:shop_cart')
    
    def post(self, request, order_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                order = Order.objects.get(id=order_id)
                order.description = data['description']
                order.payment_type = PaymentType.objects.get(id=data['payment_type'])
                order.save()

                user = request.user
                user.name = data['name']
                user.family = data['family']
                user.email = data['email']
                user.save()

                customer = Customer.objects.get(user=user)
                customer.phone_number = data['phone_number']
                customer.address = data['address']
                customer.save()
                messages.success(request, 'اطلاعات با موفقیت ثبت شد', 'success')
                return redirect('payments:zarinpal_payment', order_id)

            except:
                messages.error(request, 'فاکتوری با این مشخصات یاف نشد', 'danger')
                return redirect('orders:checkout', order_id)
        return redirect('orders:checkout', order_id)
 