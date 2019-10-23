from accounts.models import Perfil
from .models import Categoria, Produto, Carrinho


def categorias(request):
    categoria = Categoria.objects.all()
    return {'categorias': categoria}


def produtos(request):
    produtos = Produto.objects.all()
    return {'produtos': produtos}


def profile_pk(request):
    if not request.user.is_authenticated:
        perfil = None
    else:
        try:
            perfil = Perfil.objects.get(account=request.user)
        except Perfil.DoesNotExist:
            perfil = Perfil.objects.create(account=request.user)

    return {'profile_pk': perfil}


def carrinho(request):
    if not request.user.is_authenticated:
        carrinho = None
    else:
        try:
            carrinho = Carrinho.objects.get(cliente=request.user).produtos.all().count()
        except Carrinho.DoesNotExist:
            carrinho = Carrinho.objects.create(cliente=request.user)
            carrinho = carrinho.produtos.all().count()
    return {'carrinho': carrinho}
