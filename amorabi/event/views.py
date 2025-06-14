from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required

@login_required
def event_list(request):
    eventos = Evento.objects.filter(ativo=True).order_by('-data_inicio')
    return render(request, 'event/lista_todos.html', {'eventos': eventos})

@login_required
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.responsavel = request.user
            evento.save()
            return redirect('event:event_list')
    else:
        form = EventoForm()
    return render(request, 'event/cadastro.html', {'form': form})