# Generated by Django 4.2.3 on 2023-12-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_alter_customer_project_details_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_skills',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
