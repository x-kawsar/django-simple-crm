# Generated by Django 4.2.3 on 2023-08-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_order_tags_product_description_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Out For Delivery', 'Out For Delivery')], max_length=5000, null=True),
        ),
    ]
