from .models import Categoria, Produto


def categorias(request):
    categoria = Categoria.objects.all()
    return {'categorias': categoria}


def produtos(request):
    produtos = Produto.objects.all()
    return {'produtos': produtos}
