from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, CategoriaEvento, Participacao
from .forms import EventoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q, F, IntegerField, ExpressionWrapper

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

    # Eventos em que o usuário está inscrito
    eventos_inscritos = set()
    if request.user.is_authenticated:
        eventos_inscritos = set(
            Participacao.objects.filter(usuario=request.user, evento__in=eventos)
            .values_list('evento__uuid', flat=True)
        )

    # Annotate with vagas_disponiveis
    eventos = eventos.annotate(
        inscritos_confirmados=Count('participacoes', filter=Q(participacoes__status='confirmada', participacoes__ativo=True)),
    ).annotate(
        vagas_disponiveis=ExpressionWrapper(
            F('capacidade_participantes') - F('inscritos_confirmados'),
            output_field=IntegerField()
        )
    )

    return render(request, 'event/lista_todos.html', {
        'eventos': eventos,
        'categorias': categorias,
        'eventos_inscritos': eventos_inscritos,
        'current_filters': {
            'titulo': titulo,
            'categoria': categoria,
            'local': local,
            'status': status,
            'ordering': ordering,
        }
    })

@login_required
@permission_required('event.add_evento', raise_exception=True)
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
    inscrito = Participacao.objects.filter(usuario=request.user, evento=evento).exists()
    inscricao_aberta = timezone.now() <= evento.data_limite_inscricao
    return render(request, 'event/evento_detalhe.html', {
        'evento': evento,
        'inscrito': inscrito,
        'inscricao_aberta': inscricao_aberta,
    })

@login_required
def participar_evento(request, uuid):
    evento = get_object_or_404(Evento, uuid=uuid, ativo=True)
    user = request.user

    # Check if already registered
    if Participacao.objects.filter(usuario=user, evento=evento).exists():
        messages.warning(request, "Você já está inscrito neste evento.")
        return redirect('event:evento_detail', uuid=evento.uuid)

    # Check if registration is still open
    if timezone.now() > evento.data_limite_inscricao:
        messages.error(request, "O prazo de inscrição para este evento já terminou.")
        return redirect('event:evento_detail', uuid=evento.uuid)

    Participacao.objects.create(usuario=user, evento=evento)
    messages.success(request, "Inscrição realizada com sucesso!")
    return redirect('event:evento_detail', uuid=evento.uuid)