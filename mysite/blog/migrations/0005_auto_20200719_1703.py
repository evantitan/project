# Generated by Django 3.0.7 on 2020-07-19 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200719_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='auth_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='username',
        ),
    ]
