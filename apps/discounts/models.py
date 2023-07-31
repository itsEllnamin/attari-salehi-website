from uuid import uuid4
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product



cascade = models.CASCADE

class DiscountBasket(models.Model):
    title = models.CharField(_('عنوان سبد تخفیف'), max_length=70)
    start_datetime = models.DateTimeField(_('تاریخ شروع'))
    end_datetime = models.DateTimeField(_('تاریخ پایان'))
    discount_percent = models.PositiveIntegerField(_('درصد تخفیف'), validators=[MaxValueValidator(100)])
    is_active = models.BooleanField(_('وضعیت فعال/غیرفعال'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('سبد تخفیف')
        verbose_name_plural = _('سبدهای تخفیف')


class DiscountBasketDetail(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, cascade, verbose_name=_('سبد تخفیف'), related_name='discount_basket_details')
    product = models.ForeignKey(Product, cascade, verbose_name=_('کالا'), related_name='discount_basket_details')
    
    def __str__(self):
        return f'{self.discount_basket} : {self.product}'

    class Meta:
        verbose_name = _('جزئیات سبد تخفیف')
        verbose_name_plural = _('جزئیات سبد تخفیف')


class DiscountCode(models.Model):
    discount_code = models.CharField(_('کد تخفیف'), max_length=10, unique=True)
    start_datetime = models.DateTimeField(_('تاریخ شروع'))
    end_datetime = models.DateTimeField(_('تاریخ پایان'))
    discount_percent = models.PositiveIntegerField(_('درصد تخفیف'), validators=[MaxValueValidator(100)])
    is_active = models.BooleanField(_('وضعیت فعال/غیرفعال'), default=False)

    def __str__(self):
        return self.discount_code

    class Meta:
        verbose_name = _('کد تخفیف')
        verbose_name_plural = _('کدهای تخفیف')