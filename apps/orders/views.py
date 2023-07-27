from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import TemplateView
from apps.products.models import Product
from utils import page_path, partial_path, factor_details
from .shop_cart import ShopCart


appname = "orders"
# =============================================== Shop Cart ==================================================
# ======================================= Partials ==========================================


class ShopCartDetail(TemplateView):
    template_name = partial_path(appname, "shop_cart_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_cart"] = shop_cart = ShopCart(self.request)
        context["total_price"] = total_price = shop_cart.calc_total_price()
        context["delivery_cost"], context["tax"], context["final_price"] = factor_details(total_price)
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
