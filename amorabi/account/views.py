from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm
from .models import CustomUser, Aprovacao

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
    return render(request, 'account/aprovacoes.html', {'users': users_sem_aprovacao})