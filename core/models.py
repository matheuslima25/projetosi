from django.db import models
from django.utils.translation import ugettext as _

from core.choices import (
    PLATAFORM_CHOICES, OS_CHOICES,
)


class Produto(models.Model):
    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    nome = models.CharField(_('Nome'), max_length=125)
    codigo = models.CharField(_('Nome'), max_length=125)
    descricao = models.TextField(_('Nome'))
    preco = models.DecimalField(_('Nome'), decimal_places=2, max_digits=10)
    plataforma = models.CharField(_('Plataforma de Ativação'), max_length=10, choices=PLATAFORM_CHOICES)
    os = models.CharField(_('Sistemas Operacionais'), max_length=7, choices=OS_CHOICES)
    video = models.URLField(_('Vídeo'), null=True, blank=True)
    image = models.FileField(_('Imagens'), upload_to='images/')
    destaque = models.BooleanField(_('Destaque'), default=False)

    def save(self, *args, **kwargs):
        # Para apenas um Produto em destaque

        if self.destaque:
            try:
                temp = Produto.objects.get(destaque=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Produto.DoesNotExist:
                pass
