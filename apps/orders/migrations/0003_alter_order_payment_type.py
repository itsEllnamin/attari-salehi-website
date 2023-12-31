# Generated by Django 4.2 on 2023-07-27 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_order_order_status_order_payment_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_type",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="orders.paymenttype",
                verbose_name="روش پرداخت",
            ),
            preserve_default=False,
        ),
    ]
