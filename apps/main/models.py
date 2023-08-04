from django.db import models
import utils
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _



class Slider(models.Model):
    title1 = models.CharField(_("متن اول"), max_length=200, null=True, blank=True)
    title2 = models.CharField(_("متن دوم"), max_length=200, null=True, blank=True)
    title3 = models.CharField(_("متن سوم"), max_length=200, null=True, blank=True)
    file_manager = utils.FileManager('images', 'main', 'slider')
    image = models.ImageField(_("تصویر اسلاید"), upload_to=file_manager.upload_to)
    slider_link = models.URLField(_("لینک اسلاید"), max_length=200, null=True, blank=True)
    is_active = models.BooleanField(_("فعال/غیرفعال"), default=True, blank=True)
    register_datetime = models.DateTimeField(_('تاریخ درج'), auto_now_add=True)
    publish_datetime = models.DateTimeField(_('تاریخ انتشار'), default=timezone.now)
    update_datetime = models.DateTimeField(_('تاریخ آخرین بروزرسانی'), auto_now=True)
    
    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلایدها"
    
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image}" style="width:80px;height:80px;">')
    image_slide.short_description = 'تصویر اسلاید'

    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">link</a>')
    link.short_description = 'پیوندها'