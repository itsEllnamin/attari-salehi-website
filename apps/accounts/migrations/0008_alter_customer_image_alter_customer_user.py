# Generated by Django 4.2 on 2023-07-28 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_alter_customer_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=utils.FileManager.upload_to,
                verbose_name="تصویر پروفایل",
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
    ]
