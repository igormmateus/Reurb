# Generated by Django 4.1 on 2022-09-23 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0005_alter_bairro_bairro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bairro',
            name='bairro',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='precadastroimovel',
            name='bairro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cadastro.bairro'),
        ),
    ]
