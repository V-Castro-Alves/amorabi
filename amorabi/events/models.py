from django.db import models
import uuid

class Evento(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    capacidade_participantes = models.IntegerField()
    responsavel = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='evento_responsavel')
    status = models.CharField(
        max_length=20,
        choices=[
            ('nao_iniciado', 'Não Iniciado'),
            ('ativo', 'Ativo'),
            ('encerrado', 'Encerrado'),
            ('suspenso', 'Suspenso'),
        ],
        default='nao_iniciado'
    )
    local = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data_inicio']

class Participacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='participacoes')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='participacoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    presenca = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario.username} em {self.evento.titulo}'

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

