from .models import Categoria, Produto, Carrinho


def categorias(request):
    categoria = Categoria.objects.all()
    return {'categorias': categoria}


def produtos(request):
    produtos = Produto.objects.all()
    return {'produtos': produtos}


def carrinho(request):
    if not request.user.is_authenticated:
        carrinho = None
    else:
        carrinho = Carrinho.objects.filter(cliente=request.user).count()
    return {'carrinho': carrinho}
