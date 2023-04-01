# Generated by Django 4.1.3 on 2023-03-27 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_items_item_order_order_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order'),
        ),
    ]