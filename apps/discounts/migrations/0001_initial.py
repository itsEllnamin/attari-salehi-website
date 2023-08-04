# Generated by Django 4.2 on 2023-07-29 21:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (
            "products",
            "0013_alter_product_main_image_alter_productcategory_image_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscountBasket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=70, verbose_name="عنوان سبد تخفیف"),
                ),
                ("start_datetime", models.DateTimeField(verbose_name="تاریخ شروع")),
                ("end_datetime", models.DateTimeField(verbose_name="تاریخ پایان")),
                (
                    "discount_percent",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(100)],
                        verbose_name="درصد تخفیف",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="وضعیت فعال/غیرفعال"
                    ),
                ),
            ],
            options={
                "verbose_name": "سبد تخفیف",
                "verbose_name_plural": "سبدهای تخفیف",
            },
        ),
        migrations.CreateModel(
            name="DiscountCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "discount_code",
                    models.CharField(
                        default=uuid.uuid4,
                        max_length=10,
                        unique=True,
                        verbose_name="کد تخفیف",
                    ),
                ),
                ("start_datetime", models.DateTimeField(verbose_name="تاریخ شروع")),
                ("end_datetime", models.DateTimeField(verbose_name="تاریخ پایان")),
                (
                    "discount_percent",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(100)],
                        verbose_name="درصد تخفیف",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="وضعیت فعال/غیرفعال"
                    ),
                ),
            ],
            options={
                "verbose_name": "کد تخفیف",
                "verbose_name_plural": "کدهای تخفیف",
            },
        ),
        migrations.CreateModel(
            name="DiscountBasketDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "discount_basket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discount_basket_details",
                        to="discounts.discountbasket",
                        verbose_name="سبد تخفیف",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discount_basket_details",
                        to="products.product",
                        verbose_name="کالا",
                    ),
                ),
            ],
            options={
                "verbose_name": "جزئیات سبد تخفیف",
                "verbose_name_plural": "جزئیات سبد تخفیف",
            },
        ),
    ]