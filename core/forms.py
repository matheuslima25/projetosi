from django.contrib.auth.forms import forms

from core.choices import PLATAFORM_CHOICES, OS_CHOICES
from core.models import Produto


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['destaque'].help_text = 'Ao colocar como verdadeiro, a vídeo (caso possua) ou imagem fica como destaque na página inicial.'

    plataforma = forms.MultipleChoiceField(choices=PLATAFORM_CHOICES, widget=forms.CheckboxSelectMultiple, label='Plataformas de Ativação')
    os = forms.MultipleChoiceField(choices=OS_CHOICES, widget=forms.CheckboxSelectMultiple, label='Sistemas Operacionais')

    class Meta:
        model = Produto
        fields = '__all__'
