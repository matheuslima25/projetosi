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
        perfil = Perfil.objects.get(account=request.user)

    return {'profile_pk': perfil}


def carrinho(request):
    if not request.user.is_authenticated:
        carrinho = None
    else:
        carrinho = Carrinho.objects.get(cliente=request.user).produtos.all().count()
    return {'carrinho': carrinho}
