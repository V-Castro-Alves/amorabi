from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titulo', 'descricao', 'data_inicio', 'data_fim', 'data_limite_inscricao', 'capa', 'capacidade_participantes', 'local'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy HH:MM'},
                format='%d/%m/%Y %H:%M'
            ),
            'data_fim': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy HH:MM'},
                format='%d/%m/%Y %H:%M'
            ),
            'data_limite_inscricao': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'dd/mm/yyyy HH:MM'},
                format='%d/%m/%Y %H:%M'
            ),
            'capa': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'capacidade_participantes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['data_inicio', 'data_fim']:
            self.fields[field].input_formats = ['%d/%m/%Y %H:%M']
            if self.instance.pk:
                value = getattr(self.instance, field)
                if value:
                    self.fields[field].initial = value.strftime('%d/%m/%Y %H:%M')