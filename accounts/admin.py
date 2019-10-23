from django.contrib import admin

from accounts.models import Account, Endereco, Perfil


@admin.register(Account)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_login')


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('account', 'ultimo_acesso',)
    readonly_fields = ('ultimo_acesso',)

