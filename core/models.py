from django.db import models
from django.utils.translation import ugettext as _
from multiselectfield import MultiSelectField

from core.choices import (
    PLATAFORM_CHOICES, OS_CHOICES,
)


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
    image = models.FileField(_('Imagens'), upload_to='images/')
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
