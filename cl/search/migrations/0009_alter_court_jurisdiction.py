# Generated by Django 3.2.16 on 2022-11-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_fix_on_delete_noop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='jurisdiction',
            field=models.CharField(choices=[('F', 'Federal Appellate'), ('FD', 'Federal District'), ('FB', 'Federal Bankruptcy'), ('FBP', 'Federal Bankruptcy Panel'), ('FS', 'Federal Special'), ('S', 'State Supreme'), ('SA', 'State Appellate'), ('ST', 'State Trial'), ('SS', 'State Special'), ('TRS', 'Tribal Supreme'), ('TRA', 'Tribal Appellate'), ('TRT', 'Tribal Trial'), ('TRX', 'Tribal Special'), ('TS', 'Territory Supreme'), ('TA', 'Territory Appellate'), ('TT', 'Territory Trial'), ('TSP', 'Territory Special'), ('SAG', 'State Attorney General'), ('C', 'Committee'), ('I', 'International'), ('T', 'Testing')], help_text='the jurisdiction of the court, one of: F (Federal Appellate), FD (Federal District), FB (Federal Bankruptcy), FBP (Federal Bankruptcy Panel), FS (Federal Special), S (State Supreme), SA (State Appellate), ST (State Trial), SS (State Special), TRS (Tribal Supreme), TRA (Tribal Appellate), TRT (Tribal Trial), TRX (Tribal Special), TS (Territory Supreme), TA (Territory Appellate), TT (Territory Trial), TSP (Territory Special), SAG (State Attorney General), C (Committee), I (International), T (Testing)', max_length=3),
        ),
    ]