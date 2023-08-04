from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _



cascade = models.CASCADE

class TransactionType(models.Model):
    title = models.CharField(_('نوع تراکنش'), max_length=50)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('نوع تراکنش')
        verbose_name_plural = _('انواع تراکنش')

        
class Transaction(models.Model):
    type = models.ForeignKey(TransactionType, cascade, related_name='transactions', verbose_name=_('نوع تراکنش'))
    user_registered = models.ForeignKey(CustomUser, cascade, related_name='transactions', verbose_name=_('کاربر ثبت‌کننده'))
    product = models.ForeignKey(Product, cascade, related_name='transactions', verbose_name=_('کالا'))
    qty = models.PositiveIntegerField(_('تعداد'))
    price = models.PositiveIntegerField(_('قیمت واحد'), null=True, blank=True)
    register_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))

    def __str__(self):
        return f'{self.type} - {self.product} - {self.qty}'

    class Meta:
        verbose_name = _('تراکنش')
        verbose_name_plural = _('تراکنش‌ها')

        
