from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4



cascade = models.CASCADE

class PaymentType(models.Model):
    payment_type = models.CharField(_('نوع پرداخت'), max_length=60)

    def __str__(self):
        return self.payment_type
    
    class Meta:
        verbose_name = 'روش پرداخت'
        verbose_name_plural = 'انواع روش‌های پرداخت'


class OrderStatus(models.Model):
    status = models.CharField(_('وضعیت سفارش'), max_length=60)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'انواع وضعیت‌های سفارش'


class Order(models.Model):
    customer = models.ForeignKey(Customer, cascade, verbose_name=_('مشتری'), related_name='orders')
    register_datetime = models.DateTimeField(_("تاریخ ثبت سفارش"), default=timezone.now)
    update_datetime = models.DateTimeField(_("تاریخ آخرین ویرایش"), auto_now=True)
    is_finally = models.BooleanField(default=False, verbose_name='نهایی شده')
    order_code = models.UUIDField(_("کد سفارش"), unique=True, default=uuid4, editable=False)
    discount = models.PositiveIntegerField(_('درصد تخفیف روی سفارش'), default=0, null=True)
    description = models.TextField(_('توضیحات'), blank=True, null=True)

    def __str__(self):
        return f'{self.customer}\t{self.id}\t{self.is_finaly}'

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارشات')


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, cascade, related_name='order_details', verbose_name=_('سفارش'))
    product = models.ForeignKey(Product, cascade, related_name='order_details', verbose_name=_('کالا'))
    qty = models.PositiveIntegerField(_('تعداد'), default=1)
    price = models.PositiveIntegerField(_('قیمت کالا در فاکتور'), default=0)

    def __str__(self):
        return f'{self.order}\t{self.product}\t{self.qty}\t{self.price}'
