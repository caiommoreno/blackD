# Generated by Django 3.1.1 on 2020-09-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=100)),
                ('cliente', models.CharField(max_length=100)),
                ('total', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='preco_custo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='preco_venda',
            field=models.CharField(max_length=100),
        ),
    ]