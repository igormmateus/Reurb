# Generated by Django 4.1 on 2022-08-29 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CadastroPessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('rg', models.CharField(max_length=30)),
                ('orgao_rg', models.CharField(max_length=10)),
                ('estado_rg', models.CharField(max_length=2)),
                ('nome_pai', models.CharField(max_length=255)),
                ('nome_mae', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=14)),
                ('profissao', models.CharField(max_length=50)),
                ('estado_civil', models.CharField(choices=[('C', 'Casado(a)'), ('S', 'Solteiro(a)'), ('V', 'Viuvo(a)'), ('D', 'Divorciada(a)')], max_length=1)),
            ],
        ),
    ]
