from django.db import models
from django.utils import timezone
from utils import FileManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime
from django.db.models import Avg, Sum
from middlewares.middlewares import RequestMiddleware



app_name = "product_app"


# class Brand(models.Model):
#     title = models.CharField(_("عنوان برند"), max_length=100)
#     file_manager = FileManager("images", app_name, "brands")
#     logo = models.ImageField(_("لوگو"), upload_to=file_manager.upload_to)
#     slug = models.SlugField(_('اسلاگ'), max_length=150)
#     is_active = models.BooleanField(_("وضعیت فعال/غیرفعال"), default=True, blank=True)
#     register_datetime = models.DateTimeField(_("تاریخ درج"), auto_now_add=True)
#     update_datetime = models.DateTimeField(_("تاریخ آخرین بروزرسانی"), auto_now=True)
#     publish_datetime = models.DateTimeField(_("تاریخ انتشار"), default=timezone.now)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = _("برند")
#         verbose_name_plural = _("برندها")


class ProductCategory(models.Model):
    title = models.CharField(_("عنوان دسته‌ی کالا"), max_length=100)
    file_manager = FileManager("images", app_name, "product_categories")
    image = models.ImageField(_("تصویر اصلی دسته"), upload_to=file_manager.upload_to)
    description = models.TextField(_("توضیحات دسته"), blank=True, null=True)
    subset_of = models.ForeignKey(
        "ProductCategory",
        models.CASCADE,
        verbose_name=_("زیرمجموعه‌ی"),
        related_name="subsets",
        blank=True,
        null=True,
    )
    slug = models.SlugField(_("اسلاگ"), max_length=150)
    is_active = models.BooleanField(_("وضعیت فعال/غیرفعال"), default=True, blank=True)
    register_datetime = models.DateTimeField(_("تاریخ درج"), auto_now_add=True)
    update_datetime = models.DateTimeField(_("تاریخ آخرین بروزرسانی"), auto_now=True)
    publish_datetime = models.DateTimeField(_("تاریخ انتشار"), default=timezone.now)

    def get_absolute_url(self):
        return reverse("products:product_category", kwargs={"slug": self.slug})

    # برگرداندن دسته‌بندی‌های ریشه 
    @classmethod
    def get_root_categories(cls): 
        return cls.objects.filter(subset_of=None, is_active=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("دسته‌ی کالا")
        verbose_name_plural = _("دسته‌های کالا")


class Feature(models.Model):
    name = models.CharField(_("نام ویژگی"), max_length=100)
    categories = models.ManyToManyField(
        ProductCategory,
        verbose_name=_("دسته‌ی کالا"),
        related_name="features",
    )
    is_active = models.BooleanField(_("وضعیت فعال/غیرفعال"), default=True, blank=True)
    register_datetime = models.DateTimeField(_("تاریخ درج"), auto_now_add=True)
    update_datetime = models.DateTimeField(_("تاریخ آخرین بروزرسانی"), auto_now=True)
    publish_datetime = models.DateTimeField(_("تاریخ انتشار"), default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("ویژگی")
        verbose_name_plural = _("ویژگی‌ها")


class FeatureDigitalValue(models.Model):
    value = models.CharField(_("مقدار"), max_length=60)
    feature = models.ForeignKey(
        Feature, models.CASCADE, verbose_name=_("ویژگی"), related_name="digital_values"
    )

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _("مقدار دیجیتال ویژگی")
        verbose_name_plural = _("مقادیر دیجیتال ویژگی")


class Product(models.Model):
    name = models.CharField(_("نام کالا"), max_length=150)
    short_text = models.TextField(_("خلاصه توضیحات کالا"), blank=True, null=True)
    text = RichTextUploadingField(
        _("توضیحات کالا"), blank=True, null=True, config_name="default"
    )
    price = models.PositiveIntegerField(_("بهای کالا"), default=0)
    file_manager = FileManager("images", app_name, "products")
    main_image = models.ImageField(_("تصویر اصلی"), upload_to=file_manager.upload_to)
    category = models.ForeignKey(
        ProductCategory,
        models.CASCADE,
        verbose_name=_("دسته‌ی کالا"),
        related_name="category_products",
    )
    # brand = models.ForeignKey(
    #     Brand,
    #     models.CASCADE,
    #     verbose_name=_("برند کالا"),
    #     blank=True,
    #     null=True,
    #     related_name="products",
    # )
    features = models.ManyToManyField(
        Feature,
        through="ProductFeature",
        verbose_name=_("ویژگی‌های کالا"),
        related_name="products",
    )
    slug = models.SlugField(_("اسلاگ"), max_length=150)
    is_active = models.BooleanField(_("وضعیت فعال/غیرفعال"), default=True, blank=True)
    register_datetime = models.DateTimeField(_("تاریخ درج"), auto_now_add=True)
    update_datetime = models.DateTimeField(_("تاریخ آخرین بروزرسانی"), auto_now=True)
    publish_datetime = models.DateTimeField(_("تاریخ انتشار"), default=timezone.now)

    def get_absolute_url(self):
        return reverse("products:product", kwargs={"slug": self.slug})
    
    # برگرداندن قیمت نهایی کالا با احتساب تخفیف‌ سبد تخفیف
    def get_discounted_price(self):
        list1 = []
        disount_details = self.discount_basket_details.all()
        for disount_detail in disount_details:
            if  ((db:=disount_detail.discount_basket).is_active  and
                db.start_datetime <= datetime.now()  and
                datetime.now() <= db.end_datetime):
                list1.append (db.discount_percent)
        discount = 0
        if  len(list1) > 0  :
            discount = max(list1)
        discount_amount  =  self.price * discount / 100
        discounted_price  =  self.price - int(discount_amount)
        return discounted_price 

    # برگرداندن میانگین امتیازات محصول
    def get_avg_score(self):
        avg_score = self.scores.all().aggregate(Avg('score'))['score__avg']
        if not avg_score:
            avg_score = 0
        return avg_score

    # برگرداندن امتیازی که کاربر جاری به این کالا داده
    def get_current_user_score(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user = self.scores.filter(user=request.user)
        if  user.count() > 0  :
            score = user[0].score
        return score

    def is_user_favorite(self):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        flag = self.favorites.filter(user=request.user).exists()
        return flag   

    # تعداد موجودی کالا در انبار
    def get_quantity_in_warehouse(self):
        input = self.transactions.filter(type__title__contains='خرید').aggregate(Sum('qty'))
        output = self.transactions.filter(type__title__contains='فروش').aggregate(Sum('qty'))
        inputs = 0
        if (inputs_sum:=input['qty__sum']):
            inputs = inputs_sum
        outputs = 0
        if (outputs_sum:=output['qty__sum']):
            outputs = outputs_sum
        return inputs - outputs

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("کالا")
        verbose_name_plural = _("کالاها")


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, models.CASCADE, verbose_name=_("کالا"), related_name="product_features"
    )
    feature = models.ForeignKey(
        Feature,
        models.CASCADE,
        verbose_name=_("ویژگی"),
        related_name="product_features",
    )
    analogue_value = models.CharField(
        _("مقدار آنالوگ"), max_length=100, blank=True, null=True
    )
    digital_value = models.ForeignKey(
        FeatureDigitalValue,
        models.CASCADE,
        verbose_name=_("مقدار دیجیتال"),
        related_name="product_features",
    )

    def __str__(self):
        return f"ویژگی {self.feature} برای کالای {self.product} برابر است با: {self.digital_value}"

    class Meta:
        verbose_name = _("ویژگی کالا")
        verbose_name_plural = _("ویژگی‌های کالا")


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, models.CASCADE, verbose_name=_("کالا"), related_name="images"
    )
    file_manager = FileManager("images", app_name, "products")
    images = models.ImageField(_("تصویر"), upload_to=file_manager.upload_to)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = _("تصویر کالا")
        verbose_name_plural = _("تصاویر کالا")
