# Generated by Django 5.1.6 on 2025-03-04 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recommended_doctor',
            field=models.CharField(blank=True, max_length=50, verbose_name='Tavsiya etilgan shifokor'),
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Dori nomi')),
                ('timing', models.CharField(max_length=100, verbose_name='Ichish vaqti (masalan, abedda ertalab)')),
                ('start_date', models.DateField(verbose_name='Boshlanish sanasi')),
                ('end_date', models.DateField(verbose_name='Tugash sanasi')),
                ('instructions', models.TextField(blank=True, verbose_name='Qo‘shimcha ko‘rsatmalar')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile', verbose_name='Foydalanuvchi profili')),
            ],
        ),
    ]
