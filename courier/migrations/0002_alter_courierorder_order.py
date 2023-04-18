# Generated by Django 4.1.3 on 2023-04-15 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_status'),
        ('courier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_order', to='order.order'),
        ),
    ]
