from .models import Categoria


def categorias(request):
    categoria = Categoria.objects.all()
    return {'categorias': categoria}


def plataformas(request):
    plataformas = Categoria.objects.all()
    return {'categorias': categoria}
