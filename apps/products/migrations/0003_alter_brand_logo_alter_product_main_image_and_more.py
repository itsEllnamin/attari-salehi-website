# Generated by Django 4.2 on 2023-07-10 12:04

from django.db import migrations, models
import utils


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_remove_brand_image_brand_logo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="logo",
            field=models.ImageField(
                upload_to=utils.FileManager.upload_to, verbose_name="لوگو"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="main_image",
            field=models.ImageField(
                upload_to=utils.FileManager.upload_to, verbose_name="تصویر اصلی"
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="image",
            field=models.ImageField(
                upload_to=utils.FileManager.upload_to, verbose_name="تصویر اصلی دسته"
            ),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="images",
            field=models.ImageField(
                upload_to=utils.FileManager.upload_to, verbose_name="تصویر"
            ),
        ),
    ]
