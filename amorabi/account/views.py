from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm
from .models import CustomUser, StatusUsuario

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('account:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/cadastro.html', {'form': form})

@login_required
def aprovacoes(request):
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        return HttpResponseForbidden("Acesso restrito a administradores.")
    users_sem_aprovacao = CustomUser.objects.filter(
        is_superuser=False
    ).exclude(
        aprovacoes__isnull=False
    )
    return render(request, 'account/aprovacao.html', {'users': users_sem_aprovacao})

@login_required
def aprovacao_detalhe(request, user_uuid):
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        return HttpResponseForbidden("Acesso restrito a administradores.")
    user = get_object_or_404(CustomUser, uuid=user_uuid, is_superuser=False)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            StatusUsuario.objects.create(
                usuario=user,
                status='aprovado',
                responsavel=request.user
            )
            messages.success(request, 'Usuário aprovado!')
        elif action == 'disapprove':
            StatusUsuario.objects.create(
                usuario=user,
                status='rejeitado',
                responsavel=request.user
            )
            messages.success(request, 'Usuário reprovado!')
        return redirect('account:aprovacoes')
    return render(request, 'account/aprovacao_detalhe.html', {'user': user})

def resetar_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(CustomUser, email=email)
        # Lógica para enviar e-mail de redefinição de senha
        messages.success(request, 'Instruções de redefinição de senha enviadas para o seu e-mail.')
        return redirect('account:login')
    return render(request, 'account/resetar_senha.html')