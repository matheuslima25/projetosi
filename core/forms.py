from django.contrib.auth.forms import forms

from core.models import Produto


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['destaque'].help_text = 'Ao colocar como verdadeiro, a vídeo (caso possua) ou imagem fica como destaque na página inicial.'

    class Meta:
        model = Produto
        fields = '__all__'
