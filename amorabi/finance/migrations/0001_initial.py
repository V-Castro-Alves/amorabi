# Generated by Django 5.2.1 on 2025-06-25 21:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentroCusto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Centro de Custo',
                'verbose_name_plural': 'Centros de Custo',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='MovimentacaoFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('descricao', models.TextField(blank=True, help_text='Descrição da movimentação financeira')),
                ('valor', models.IntegerField(help_text='Valor em centavos')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=50)),
                ('ativo', models.BooleanField(default=True, help_text='Indica se a movimentação está ativa')),
                ('centro_custo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes', to='finance.centrocusto')),
            ],
            options={
                'verbose_name': 'Movimentação Financeira',
                'verbose_name_plural': 'Movimentações Financeiras',
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='MovimentacaoFinanceiraEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ativo', models.BooleanField(default=True, help_text='Indica se a movimentação financeira por evento está ativa')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentacoes_financeiras', to='event.evento')),
                ('movimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='finance.movimentacaofinanceira')),
            ],
            options={
                'verbose_name': 'Movimentação Financeira por Evento',
                'verbose_name_plural': 'Movimentações Financeiras por Evento',
            },
        ),
    ]
