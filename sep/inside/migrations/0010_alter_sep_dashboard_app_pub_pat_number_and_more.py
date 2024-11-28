# Generated by Django 5.1 on 2024-11-05 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inside', '0009_alter_sep_dashboard_ess_to_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sep_dashboard',
            name='App_pub_pat_Number',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Application_Number',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='COMMITTEE',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='COUNTRY_CODE',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Current_Assignee',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='DIPG_EXTERNAL_ID',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='ILLUSTRATIVE_PART',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='IPRD_REFERENCE',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Inventor',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='PATENT_OWNER',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Patent_Number',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Publication_Number',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='RECOMMENDATION',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='STANDARD',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='STANDARD_SETTING',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Sub_Technology',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Technology',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Title',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='sep_dashboard',
            name='Type',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
