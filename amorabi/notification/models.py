from django.db import models
import uuid

class Notificacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=[
        ('seguranca', 'Segurança'),
        ('sistema', 'Sistema')
    ])
    canal = models.CharField(max_length=50, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('app', 'Aplicativo')
    ])
    data_criacao = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f'Notificação para {self.usuario.username} - {self.mensagem[:50]}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('notificacao_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_criacao']