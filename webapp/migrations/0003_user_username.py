# Generated by Django 4.2.2 on 2023-06-20 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_user_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
