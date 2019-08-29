from django.contrib.auth.forms import forms

from core.models import Produto


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['destaque'].help_text = 'Ao marcar, a vídeo (caso possua) ou imagem fica como destaque na página inicial.'
        self.fields['promocao'].help_text = 'Ao marcar, o produto ficará com uma etiqueta de promoção.'
        self.fields['propaganda'].help_text = 'Ao marcar, o produto ficará em um banner no fim da página.'

    class Meta:
        model = Produto
        fields = '__all__'
