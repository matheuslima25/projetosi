from django.contrib.auth import get_user_model
from django.contrib.auth.forms import forms, UserCreationForm
from django.db.models import Q

from accounts.models import Account, Perfil
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


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if Account.objects.filter(Q(email=email)).exists():
            raise forms.ValidationError(u'Já existe um usuário com este email.')
        return email

    def save(self, commit=True):
        account = super(UserCreateForm, self).save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()

        Perfil.objects.create(account=account)
        return account
