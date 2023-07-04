from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        mobile_number,
        password,
        activation_code=None,
        email="",
        name="",
        family="",
    ):
        if not mobile_number:
            raise ValueError("شماره موبایل باید وارد شود.")

        user = self.model(
            mobile_number=mobile_number,
            activation_code=activation_code,
            email=self.normalize_email(email),
            name=name,
            family=family,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password, email, name, family):
        user = self.create_user(mobile_number, password, email, name, family)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number_validator = RegexValidator(
        regex=r"^09\d{9}", message="شماره موبایل وارد شده معتبر نیست"
    )

    mobile_number = models.CharField(
        _("شماره موبایل"),
        max_length=11,
        unique=True,
        validators=[mobile_number_validator],
    )
    name = models.CharField(_("نام"), max_length=50, blank=True)
    family = models.CharField(_("نام‌خانوادگی"), max_length=50, blank=True)
    email = models.EmailField(_("ایمیل"), blank=True)
    is_staff = models.BooleanField(_("وضعیت ادمینی"), default=False)
    is_active = models.BooleanField(_("وضعیت فعال/غیرفعال"), default=False)
    datetime_joined = models.DateTimeField(_("تاریخ ثبت‌نام"), default=timezone.now)
    activation_code = models.CharField(
        _("کد فعالسازی"), max_length=100, null=True, blank=True
    )

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["email", "name", "family"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name + " " + self.family

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
