# Generated by Django 3.1.5 on 2021-04-29 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210202_0754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('email', models.CharField(default='', max_length=30)),
                ('phone', models.CharField(default='', max_length=20)),
                ('desc', models.CharField(default='', max_length=400)),
            ],
        ),
    ]