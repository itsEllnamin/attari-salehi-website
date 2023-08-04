from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


cascade = models.CASCADE


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        cascade,
        related_name="comments",
        verbose_name=_("کاربر نظردهنده"),
    )
    product = models.ForeignKey(
        Product, cascade, related_name="comments", verbose_name=_("کالا")
    )
    text = models.TextField(_("متن"))
    register_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ درج")
    )
    approving_user = models.ForeignKey(
        CustomUser,
        cascade,
        related_name="approved_comments",
        verbose_name=_("کاربر تاییدکننده نظر"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(_("فعال/غیرفعال"), default=False)
    reply_to = models.ForeignKey(
        "Comment",
        cascade,
        related_name="replies",
        verbose_name=_("پاسخ به"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")


class Score(models.Model):
    user = models.ForeignKey(
        CustomUser, cascade, related_name="scores", verbose_name=_("کاربر امتیاز دهنده")
    )
    product = models.ForeignKey(
        Product, cascade, related_name="scores", verbose_name=_("کالا")
    )
    register_datetime = models.DateTimeField(
        _("تاریخ درج"), auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        _("امتیاز"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def __str__(self):
        return f"{self.user} - {self.product} - {self.score}"

    class Meta:
        verbose_name = _("امتیاز")
        verbose_name_plural = _("امتیازات")


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, cascade, related_name="favorites", verbose_name=_("کاربر")
    )
    product = models.ForeignKey(
        Product, cascade, related_name="favorites", verbose_name=_("کالا")
    )
    register_datetime = models.DateTimeField(
        _("تاریخ درج"), auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        verbose_name = _("علاقه")
        verbose_name_plural = _("علایق")
