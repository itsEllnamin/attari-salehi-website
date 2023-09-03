from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



cascade = models.CASCADE

class Payment(models.Model):
    order = models.ForeignKey(Order, cascade, related_name='order_payments', verbose_name=_('سفارش'))
    customer = models.ForeignKey(Customer, cascade, related_name='customer_payments', verbose_name=_('مشتری'))
    register_datetime = models.DateTimeField(_('تاریخ پرداخت'), default=timezone.now)
    update_datetime = models.DateTimeField(_('تاریخ بروزرسانی پرداخت'), auto_now=True)
    amount = models.PositiveIntegerField(_('مبلغ پرداخت'))
    description = models.TextField(_('توضیحات پرداخت'))
    is_finally = models.BooleanField(_('وضعیت نهایی/غیرنهایی'), default=False)

    status_code = models.IntegerField(_('کد وضعیت درگاه'), blank=True, null=True)
    ref_id = models.CharField(_('شماره پیگیری پرداخت'), max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.order} {self.customer} {self.ref_id}'
    
    class Meta:
        verbose_name = _('پرداخت')
        verbose_name_plural = _('پرداخت‌ها')