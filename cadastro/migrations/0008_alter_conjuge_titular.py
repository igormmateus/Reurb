# Generated by Django 4.1 on 2022-09-26 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0007_alter_conjuge_titular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conjuge',
            name='titular',
            field=models.ForeignKey(default='last', on_delete=django.db.models.deletion.DO_NOTHING, to='cadastro.cadastropessoa'),
        ),
    ]
