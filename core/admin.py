from django.contrib import admin

from core.forms import ProductForm
from .models import Produto, Categoria, Carrinho

admin.site.site_title = 'Games4Sale'
admin.site.site_header = 'Games4Sale - Administração'


@admin.register(Produto)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('nome', 'preco', 'destaque', 'promocao', 'propaganda')
    search_fields = ('nome', )
    list_filter = ('nome', 'preco', 'destaque', 'promocao', 'propaganda')


@admin.register(Carrinho)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'aberto')
    search_fields = ('cliente', )
    list_filter = ('cliente', 'data', 'aberto')
    readonly_fields = ('data',)


admin.site.register(Categoria)


