# Generated by Django 4.2 on 2023-07-12 01:42

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):
    dependencies = [
        (
            "products",
            "0006_alter_product_main_image_alter_productcategory_image_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="featuredigitalvalue",
            name="feature",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="digital_value",
                to="products.feature",
                verbose_name="ویژگی",
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