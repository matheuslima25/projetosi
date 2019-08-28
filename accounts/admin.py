from django.contrib import admin

from accounts.models import Account, Endereco, Perfil


@admin.register(Account)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'last_login')


admin.site.register(Endereco)
admin.site.register(Perfil)
