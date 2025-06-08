from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    telefone = models.CharField(max_length=20, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('usuario', 'Usuário'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')
    ativo = models.BooleanField(default=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

class Aprovacao(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='aprovacoes')
    data_aprovacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ])
    aprovador = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='aprovacoes_realizadas')