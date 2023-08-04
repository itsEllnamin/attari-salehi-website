# Generated by Django 4.2 on 2023-08-01 21:19

from django.db import migrations, models
import utils


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0011_alter_customer_image_alter_customer_user"),
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
    ]