# Generated by Django 3.2.14 on 2022-07-15 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-created_date']},
        ),
    ]
