# Generated by Django 4.2 on 2023-07-10 12:02

from django.db import migrations, models
import utils


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="brand",
            name="image",
        ),
        migrations.AddField(
            model_name="brand",
            name="logo",
            field=models.ImageField(
                default=None, upload_to=utils.FileManager.upload_to, verbose_name="لوگو"
            ),
            preserve_default=False,
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
