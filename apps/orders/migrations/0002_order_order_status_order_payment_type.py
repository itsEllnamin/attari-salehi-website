# Generated by Django 4.2 on 2023-07-27 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_status",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="orders.orderstatus",
                verbose_name="وضعیت سفارش",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="payment_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="orders.paymenttype",
                verbose_name="روش پرداخت",
            ),
        ),
    ]
