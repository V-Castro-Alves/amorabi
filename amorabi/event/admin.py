from django.contrib import admin
from .models import Evento, Participacao

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_inicio', 'data_fim', 'status', 'local', 'responsavel')
    list_filter = ('status', 'data_inicio', 'local')
    search_fields = ('titulo', 'descricao', 'local', 'responsavel__username')
    ordering = ('-data_inicio',)

@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'data_inscricao', 'presenca', 'status')
    list_filter = ('status', 'presenca', 'data_inscricao')
    search_fields = ('usuario__username', 'evento__titulo')
    ordering = ('-data_inscricao',)