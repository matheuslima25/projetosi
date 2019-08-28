# Generated by Django 2.2.4 on 2019-08-28 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=125, verbose_name='Nome')),
                ('codigo', models.CharField(max_length=125, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Nome')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Nome')),
                ('plataforma', models.CharField(choices=[('steam', 'Steam'), ('gog', 'GOG Galaxy'), ('uplay', 'Uplay')], max_length=10, verbose_name='Plataforma de Ativação')),
                ('os', models.CharField(choices=[('windows', 'Windows'), ('linux', 'Linux'), ('macos', 'MacOS')], max_length=7, verbose_name='Sistemas Operacionais')),
                ('video', models.URLField(blank=True, null=True, verbose_name='Vídeo')),
                ('image', models.FileField(upload_to='images/', verbose_name='Imagens')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
