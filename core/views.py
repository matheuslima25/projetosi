from django.views.generic import TemplateView

from core.models import Produto, Categoria


class HomeView(TemplateView):
    model = Produto
    template_name = 'produtos/index.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['games'] = Produto.objects.all()
        context['categoria_list'] = Categoria.objects.all()
        return context
