# Generated by Django 2.2.4 on 2019-09-28 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_produto_propaganda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produtos', models.ManyToManyField(blank=True, to='core.Produto')),
            ],
            options={
                'verbose_name': 'Carrinho de Compras',
                'verbose_name_plural': 'Carrinho de Compras',
            },
        ),
    ]