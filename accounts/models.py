from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _

from accounts.choices import (
    GENERO_CHOICES, ESTADOS_CHOICES,
)


class EmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given username must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('days_access', 0)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        select_on_save = True

    username = models.CharField(max_length=191, unique=True)
    email = models.EmailField(_('Email'), max_length=191, unique=True)
    name = models.CharField(_('Nome'), max_length=60, blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.name or self.email


class Endereco(models.Model):
    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')




class Perfil(models.Model):
    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfis')
        ordering = ('account__name',)
        select_on_save = True

    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    dt_nasc = models.DateField(_('Data de nascimento'), blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=20, blank=True, null=True)
    genero = models.CharField(_('Sexo'), max_length=16, choices=GENERO_CHOICES, blank=True, null=True)
    pais = models.CharField(_('País'), max_length=20, blank=True, null=True)
    end_cep = models.CharField(_('CEP'), max_length=16, blank=True, null=True)
    end_estado = models.CharField(_('Estado'), max_length=120, blank=True, null=True, choices=ESTADOS_CHOICES)
    end_cidade = models.CharField(_('Cidade'), max_length=120, blank=True, null=True)
    end_rua = models.CharField(_('Rua'), max_length=255, blank=True, null=True)
    end_numero = models.CharField(_('Número'), max_length=10, blank=True, null=True)
    end_bairro = models.CharField(_('Bairro'), max_length=120, blank=True, null=True)
    end_complemento = models.CharField(_('Complemento'), max_length=255, blank=True, null=True)

    ultimo_acesso = models.DateTimeField(auto_now=True)

    def name(self):
        return self.account.name

    def email(self):
        return self.account.email

    def __str__(self):
        return u'%s' % self.account
