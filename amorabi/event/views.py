from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, CategoriaEvento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def event_list(request):
    eventos = Evento.objects.filter(ativo=True)
    categorias = CategoriaEvento.objects.filter(ativo=True)
    # Filtering
    titulo = request.GET.get('titulo', '').strip()
    categoria = request.GET.get('categoria', '')
    local = request.GET.get('local', '').strip()
    status = request.GET.get('status', '')
    ordering = request.GET.get('ordering', '-data_inicio')

    if titulo:
        eventos = eventos.filter(titulo__icontains=titulo)
    if categoria:
        eventos = eventos.filter(categoria__uuid=categoria)
    if local:
        eventos = eventos.filter(local__icontains=local)
    if status:
        eventos = eventos.filter(status=status)

    # Ordering
    allowed_orderings = ['data_inicio', '-data_inicio', 'data_fim', '-data_fim', 'titulo', '-titulo']
    if ordering in allowed_orderings:
        eventos = eventos.order_by(ordering)
    else:
        eventos = eventos.order_by('-data_inicio')

    return render(request, 'event/lista_todos.html', {
        'eventos': eventos,
        'categorias': categorias,
        'current_filters': {
            'titulo': titulo,
            'categoria': categoria,
            'local': local,
            'status': status,
            'ordering': ordering,
        }
    })

@login_required
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.responsavel = request.user
            evento.save()
            return redirect('event:event_list')
    else:
        form = EventoForm()
    return render(request, 'event/cadastro.html', {'form': form})

@login_required
def evento_detail(request, uuid):
    evento = get_object_or_404(Evento, uuid=uuid, ativo=True)
    return render(request, 'event/evento_detalhe.html', {'evento': evento})