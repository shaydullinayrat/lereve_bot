# Generated by Django 4.2.16 on 2024-11-29 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('care_requests', '0002_carerequestdetail_remove_carerequest_question_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carerequestdetail',
            options={'ordering': ['id'], 'verbose_name': 'Деталь запроса', 'verbose_name_plural': 'Деталь запроса'},
        ),
    ]
