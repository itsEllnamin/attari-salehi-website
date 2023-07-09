from django.db import models
from django.utils import timezone
from utils import FileManager
from ckeditor_uploader.fields import RichTextUploadingField



app_name = 'product_app'

class Brand(models.Model):
    title = models.CharField(_('عنوان برند'), max_length=100)
    file_manager = FileManager('images', app_name, 'brands')
    image = models.ImageField(_('لوگو'), upload_to=file_manager.upload_to)
    slug = models.SlugField(max_length=150)
    is_active = models.BooleanField(_('وضعیت فعال/غیرفعال'), default=True, blank=True)
    register_datetime = models.DateTimeField(_('تاریخ درج'), auto_now_add=True)
    update_datetime = models.DateTimeField(_('تاریخ آخرین بروزرسانی'), auto_now=True)
    publish_datetime = models.DateTimeField(_('تاریخ انتشار'), default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('برند')
        verbose_name_plural = _('برندها')


class Category(models.Model):
    pass


class Feature(models.Model):
    name = models.CharField(_('نام ویژگی'), max_length=100)
    category = models.ForeignKey(Category, models.CASCADE, verbose_name=_('دسته‌ی کالا'))
    is_active = models.BooleanField(_('وضعیت فعال/غیرفعال'), default=True, blank=True)
    register_datetime = models.DateTimeField(_('تاریخ درج'), auto_now_add=True)
    update_datetime = models.DateTimeField(_('تاریخ آخرین بروزرسانی'), auto_now=True)
    publish_datetime = models.DateTimeField(_('تاریخ انتشار'), default=timezone.now)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('ویژگی')
        verbose_name_plural = _('ویژگی‌ها')


class FeatureDigitalValue(models.Model):
    value = models.CharField(_('مقدار'), max_length=60)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = _('مقدار دیجیتال ویژگی')
        verbose_name_plural = _('مقادیر دیجیتال ویژگی')


class Product(models.Model):
    name = models.CharField(_('نام کالا'), max_length=150)
    short_text = models.TextField(_('خلاصه توضیحات کالا'), blank=True, null=True)
    text = RichTextUploadingField(_('توضیحات کالا'), blank=True, null=True, config_name='default')
    price = models.PositiveIntegerField(_('بهای کالا'), default=0)
    file_manager = FileManager('images', app_name, 'products')
    main_image = models.ImageField(_('تصویر اصلی'), upload_to=file_manager.upload_to)
    category = models.ForeignKey(Category, models.CASCADE, verbose_name=_('دسته‌ی کالا'),)
    brand = models.ForeignKey(Brand, models.CASCADE, verbose_name=_('برند کالا'), blank=True, null=True)
    features = models.ManyToManyField(Feature, through='ProductFeature', verbose_name=_('ویژگی‌های کالا'))
    slug = models.SlugField(max_length=150)
    is_active = models.BooleanField(_('وضعیت فعال/غیرفعال'), default=True, blank=True)
    register_datetime = models.DateTimeField(_('تاریخ درج'), auto_now_add=True)
    update_datetime = models.DateTimeField(_('تاریخ آخرین بروزرسانی'), auto_now=True)
    publish_datetime = models.DateTimeField(_('تاریخ انتشار'), default=timezone.now)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('کالا')
        verbose_name_plural = _('کالاها')


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, verbose_name=_('کالا'))
    feature = models.ForeignKey(Feature, models.CASCADE, verbose_name=_('ویژگی'))
    analogue_value = models.CharField(_('مقدار آنالوگ'), max_length=100, blank=True, null=True)
    digital_value = models.ForeignKey(FeatureDigitalValue, models.CASCADE, verbose_name=_('مقدار دیجیتال'))

    def __str__(self):
        return f"ویژگی {self.feature} برای کالای {self.product} برابر است با: {self.digital_value}"
    
    class Meta:
        verbose_name = _('ویژگی کالا')
        verbose_name_plural = _('ویژگی‌های کالا')   


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, verbose_name=_('کالا'))
    file_manager = FileManager('images', app_name, 'products')
    images = models.ImageField(_('تصویر'), upload_to=file_manager.upload_to)

    def __str__(self):
        return self.product
    
    class Meta:
        verbose_name = _('تصویر کالا')
        verbose_name_plural = _('تصاویر کالا')