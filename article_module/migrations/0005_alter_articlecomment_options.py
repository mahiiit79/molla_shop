# Generated by Django 5.0.1 on 2024-03-02 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0004_articlecomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'verbose_name': 'کامنت مقاله', 'verbose_name_plural': 'کامنت مقالات مقالات'},
        ),
    ]