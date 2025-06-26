import uuid
import os
from django.db import models

def event_image_path(instance, filename):
    """Generate unique filename using UUID"""
    ext = filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('events', filename)

class Evento(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    titulo = models.CharField(max_length=200)
    capa = models.ImageField(upload_to=event_image_path, blank=True, null=True)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    capacidade_participantes = models.IntegerField(null=True)
    data_limite_inscricao = models.DateTimeField()
    responsavel = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='eventos_responsavel')
    status = models.CharField(
        max_length=20,
        choices=[
            ('nao_iniciado', 'Não Iniciado'),
            ('em_andamento', 'Em Andamento'),
            ('encerrado', 'Encerrado'),
            ('suspenso', 'Suspenso'),
        ],
        default='nao_iniciado'
    )
    local = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)
    categorias = models.ManyToManyField('CategoriaEvento', blank=True, related_name='eventos')

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('evento_detail', args=[str(self.pk)])

    def vagas_disponiveis(self):
        inscritos = self.participacoes.filter(status='confirmada', ativo=True).count()
        if self.capacidade_participantes is not None:
            return max(self.capacidade_participantes - inscritos, 0)
        return None

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data_inicio']

class Participacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='participacoes')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='participacoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    presenca = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendente'
    )
    motivo_cancelamento = models.TextField(blank=True, null=True)
    data_cancelamento = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.usuario.username} em {self.evento.titulo}'

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

class Comentario(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='comentarios')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='comentarios')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    curtidas = models.IntegerField(default=0)

    def __str__(self):
        return f'Comentário de {self.usuario.username} no evento {self.evento.titulo}'

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_criacao']

class Avaliacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='avaliacoes')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'Avaliação de {self.usuario.username} para {self.evento.titulo}'

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ('usuario', 'evento')
        ordering = ['-data_criacao']

class CategoriaEvento(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Evento"
        verbose_name_plural = "Categorias de Evento"
        ordering = ['nome']

