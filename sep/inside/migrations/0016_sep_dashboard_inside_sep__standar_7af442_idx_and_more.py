# Generated by Django 5.1 on 2024-12-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inside', '0015_userprofile'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['STANDARD_SETTING'], name='inside_sep__STANDAR_7af442_idx'),
        ),
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['Application_Number'], name='inside_sep__Applica_7e1140_idx'),
        ),
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['Patent_Number'], name='inside_sep__Patent__1a7a43_idx'),
        ),
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['Publication_Number'], name='inside_sep__Publica_77285a_idx'),
        ),
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['Technology'], name='inside_sep__Technol_68964c_idx'),
        ),
        migrations.AddIndex(
            model_name='sep_dashboard',
            index=models.Index(fields=['Sub_Technology'], name='inside_sep__Sub_Tec_31c5bc_idx'),
        ),
    ]