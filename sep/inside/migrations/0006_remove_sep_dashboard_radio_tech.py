# Generated by Django 5.1 on 2024-09-18 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inside', '0005_rename_etpr_acronym_sep_dashboard_current_assignee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sep_dashboard',
            name='Radio_Tech',
        ),
    ]
