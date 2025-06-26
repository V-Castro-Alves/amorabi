from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError

def validar_cpf(cpf):
    """
    Valida o CPF (apenas números, 11 dígitos, cálculo dos dígitos verificadores).
    """
    if not cpf:
        return
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("CPF inválido.")

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    telefone = models.CharField(max_length=20, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('usuario', 'Usuário'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    endereco_residencial = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
    def clean(self):
        super().clean()
        if self.cpf:
            validar_cpf(self.cpf)
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['username']

class StatusUsuario(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='status_usuario')
    data_aprovacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ])
    responsavel = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='status_usuario_como_responsavel')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.status} - {self.data_aprovacao.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "Status do Usuário"
        verbose_name_plural = "Status dos Usuários"
        ordering = ['-data_aprovacao']