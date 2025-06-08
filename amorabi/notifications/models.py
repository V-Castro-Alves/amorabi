from django.db import models
import uuid

class Notificacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_criacao']