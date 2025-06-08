from django.shortcuts import render
from .models import Evento
from django.contrib.auth.decorators import login_required

@login_required
def event_list(request):
    eventos = Evento.objects.filter(status__in=['nao_iniciado', 'ativo'])
    return render(request, 'event/event_list.html', {'eventos': eventos})
