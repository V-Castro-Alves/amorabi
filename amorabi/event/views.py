from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, CategoriaEvento, Participacao
from account.models import StatusUsuario
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
    if request.user.is_authenticated:
        eventos_inscritos = set(
            Participacao.objects.filter(
                usuario=request.user,
                evento__in=eventos,
                ativo=True
            ).exclude(status='cancelada')
            .values_list('evento__uuid', flat=True)
        )
    else:
        eventos_inscritos = set()
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
    inscrito = Participacao.objects.filter(
        usuario=request.user,
        evento=evento,
        ativo=True
    ).exclude(status='cancelada').exists()
    inscricao_aberta = timezone.now() <= evento.data_limite_inscricao
    # Check if user is approved
    aprovado = (
        request.user.is_superuser or
        StatusUsuario.objects.filter(
            usuario=request.user, status='aprovado', ativo=True
        ).exists()
    )
    return render(request, 'event/evento_detalhe.html', {
        'evento': evento,
        'inscrito': inscrito,
        'inscricao_aberta': inscricao_aberta,
        'aprovado': aprovado,
    })

@login_required
def participar_evento(request, uuid):
    evento = get_object_or_404(Evento, uuid=uuid, ativo=True)
    user = request.user

    # Check if registration is still open
    if timezone.now() > evento.data_limite_inscricao:
        messages.error(request, "O prazo de inscrição para este evento já terminou.")
        return redirect('event:evento_detail', uuid=evento.uuid)

    participacao = Participacao.objects.filter(usuario=user, evento=evento).first()
    if participacao:
        if participacao.ativo and participacao.status != 'cancelada':
            messages.warning(request, "Você já está inscrito neste evento.")
            return redirect('event:evento_detail', uuid=evento.uuid)
        # Reativar participação cancelada/inativa
        participacao.ativo = True
        participacao.status = 'confirmada'
        participacao.data_cancelamento = None
        participacao.motivo_cancelamento = None
        participacao.save()
        messages.success(request, "Inscrição reativada com sucesso!")
    else:
        Participacao.objects.create(usuario=user, evento=evento, status='confirmada')
        messages.success(request, "Inscrição realizada com sucesso!")
    return redirect('event:evento_detail', uuid=evento.uuid)

@login_required
def desinscrever_evento(request, uuid):
    evento = get_object_or_404(Evento, uuid=uuid, ativo=True)
    user = request.user

    participacao = Participacao.objects.filter(usuario=user, evento=evento, ativo=True).first()
    if not participacao:
        messages.warning(request, "Você não está inscrito neste evento.")
        return redirect('event:evento_detail', uuid=evento.uuid)

    if timezone.now() > evento.data_limite_inscricao:
        messages.error(request, "O prazo para desinscrição já terminou.")
        return redirect('event:evento_detail', uuid=evento.uuid)

    participacao.ativo = False
    participacao.status = 'cancelada'
    participacao.data_cancelamento = timezone.now()
    participacao.save()
    messages.success(request, "Desinscrição realizada com sucesso!")
    return redirect('event:evento_detail', uuid=evento.uuid)