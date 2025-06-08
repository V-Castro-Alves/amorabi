from django.db import models
import uuid

class CentroCusto(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custo"
        ordering = ['nome']

class MovimentacaoFinanceira(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    descricao = models.TextField(blank=True, help_text="Descrição da movimentação financeira")
    valor = models.IntegerField(help_text="Valor em centavos")
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=[
        ('entrada', 'Entrada'),
        ('saida', 'Saída')
    ])
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.descricao} - {self.valor}'

    class Meta:
        verbose_name = "Movimentação Financeira"
        verbose_name_plural = "Movimentações Financeiras"
        ordering = ['-data']

class MovimentacaoFinanceiraEvento(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    movimentacao = models.ForeignKey(MovimentacaoFinanceira, on_delete=models.CASCADE)
    evento = models.ForeignKey('events.Evento', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movimentacao} - {self.evento}'

    class Meta:
        verbose_name = "Movimentação Financeira por Evento"
        verbose_name_plural = "Movimentações Financeiras por Evento"