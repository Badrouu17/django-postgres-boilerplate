# Generated by Django 3.0.6 on 2020-05-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('photo', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255)),
                ('password_changed_at', models.BigIntegerField(max_length=20, null=True)),
                ('password_reset_token', models.CharField(max_length=255, null=True)),
                ('password_reset_expires', models.BigIntegerField(max_length=20, null=True)),
            ],
        ),
    ]
