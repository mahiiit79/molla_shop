# Generated by Django 5.0.1 on 2024-03-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0004_productbrand_url_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.BigIntegerField(verbose_name='قیمت'),
        ),
    ]
