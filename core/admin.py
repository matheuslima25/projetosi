from django.contrib import admin

from core.forms import ProductForm
from .models import Produto

admin.site.site_title = 'Games4Sale'
admin.site.site_header = 'Games4Sale - Administração'


@admin.register(Produto)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm


