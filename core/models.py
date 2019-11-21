import datetime
from decimal import Decimal

from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from multiselectfield import MultiSelectField

from accounts.models import Account
from core.choices import (
    PLATAFORM_CHOICES, OS_CHOICES,
    MONTH_CHOICES, YEARS_CHOICES)


class Categoria(models.Model):
    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')

    nome = models.CharField(_('Nome'), max_length=125)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    nome = models.CharField(_('Nome'), max_length=125)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    codigo = models.CharField(_('Código'), max_length=125)
    descricao = models.TextField(_('Descrição'))
    preco = models.DecimalField(_('Peço'), decimal_places=2, max_digits=10)
    plataforma = MultiSelectField(_('Plataforma de Ativação'), choices=PLATAFORM_CHOICES)
    os = MultiSelectField(_('Sistemas Operacionais'), choices=OS_CHOICES)
    video = models.URLField(_('Vídeo'), null=True, blank=True)
    image = CloudinaryField(_('Imagens'))
    destaque = models.BooleanField(_('Destaque'), default=False)
    promocao = models.BooleanField(_('Promoção'), default=False)
    data = models.DateField(_('Data de Lançamento'), auto_now=True)
    propaganda = models.BooleanField(_('Propaganda'), default=False)

    def save(self, *args, **kwargs):
        # Para apenas um Produto em destaque

        if self.destaque:
            try:
                temp = Produto.objects.get(destaque=True)
                if self != temp:
                    temp.destaque = False
                    temp.save()
            except Produto.DoesNotExist:
                pass

            # Para apenas um Produto na propaganda

        if self.propaganda:
            try:
                temp = Produto.objects.get(propaganda=True)
                if self != temp:
                    temp.propaganda = False
                    temp.save()
            except Produto.DoesNotExist:
                pass

        super(Produto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    class Meta:
        verbose_name = _('Carrinho de Compras')
        verbose_name_plural = _('Carrinho de Compras')

    cliente = models.ForeignKey(Account, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, blank=True)
    data = models.DateTimeField(_('Data'), auto_now_add=True)
    aberto = models.BooleanField(_('Em aberto?'), default=True, null=True, blank=True)
    valor = models.DecimalField(_('Valor'), decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.00'))], default=0.00)

    def __str__(self):
        return 'Carrinho de Compras - %s' % self.cliente


def today():
    return datetime.date.today()


class Relatorio(models.Model):
    class Meta:
        verbose_name = _('Relatório de vendas')
        verbose_name_plural = _('Relatórios de vendas')

    titulo = models.CharField(_(u'Título'), max_length=125)
    valor = models.DecimalField(_(u'Valor'), decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.00'))], default=0.00)
    mes = models.CharField(_(u'Mês'), max_length=9, choices=MONTH_CHOICES, default=str(today().month))
    ano = models.PositiveIntegerField(_(u'Ano'), choices=YEARS_CHOICES, default=today().year)

    created_at = models.DateTimeField(_(u'Data de Criação'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Data de Atualização'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.titulo = 'Relatório - %s/%s' % (str(self.mes), str(self.ano))
        super(Relatorio, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s' % self.titulo
