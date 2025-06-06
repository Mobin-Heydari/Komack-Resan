# Generated by Django 5.2 on 2025-05-27 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0001_initial'),
        ('Services', '0003_remove_service_company_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='first_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_item_services', to='Items.firstitem', verbose_name='آیتم یک'),
        ),
        migrations.AddField(
            model_name='service',
            name='is_validated_by_receptionist',
            field=models.BooleanField(default=False, verbose_name='تایید شده توسط منشی'),
        ),
        migrations.AddField(
            model_name='service',
            name='phone',
            field=models.CharField(default=1, max_length=11, verbose_name='شماره تلفن'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='second_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_item_services', to='Items.seconditem', verbose_name='آیتم دو'),
        ),
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[('IHS', 'خدمات در منزل'), ('ICS', 'خدمات در شرکت')], default=1, max_length=3, verbose_name='نوع خدمات'),
            preserve_default=False,
        ),
    ]
