# Generated by Django 5.0.1 on 2024-03-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_sitebanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitebanner',
            name='position',
            field=models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه ی جزییات محصولات'), ('about_us', 'درباره ما'), ('articles_page', 'صفحه مقالات')], max_length=200, verbose_name='جایگاه نمایشی'),
        ),
    ]
