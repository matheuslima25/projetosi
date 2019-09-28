from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView

from core.forms import UserCreateForm
from core.models import Produto, Categoria, Carrinho


class HomeView(TemplateView):
    model = Produto
    template_name = 'produtos/index.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['games'] = Produto.objects.all().order_by('-data')
        context['categoria_list'] = Categoria.objects.all()
        return context


class ProductView(DetailView):
    model = Produto
    template_name = 'produtos/product.html'

    def post_detail(self, pk):
        product = get_object_or_404(Produto, pk=pk)
        return render(self, 'produtos/product.html', {'produto': product})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Obrigado por se registrar. Agora você está logado.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
    return render(request, 'admin/signup.html', {'form': form})


def pesquisar(request):
    termo_busca = request.GET.get('search', None)

    if termo_busca:
        search = Produto.objects.filter(nome__icontains=termo_busca)
    else:
        search = Produto.objects.all().order_by('-data')

    paginator = Paginator(search, 5)
    page = request.GET.get('page')
    try:
        search = paginator.page(page)
    except PageNotAnInteger:
        search = paginator.page(1)
    except EmptyPage:
        search = paginator.page(paginator.num_pages)
    context = {
        'search': search
    }

    return render(request, 'produtos/pesquisa.html', context)


class CarrinhoView(UpdateView):
    model = Carrinho
    template_name = 'produtos/index.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            produto = get_object_or_404(Produto, pk=self.kwargs['pk'])
            user = self.request.user
            carrinho, created = Carrinho.objects.get_or_create(cliente=user)
            carrinho.save()
            carrinho.produtos.add(produto)
            return HttpResponseRedirect(reverse('index'))
        return super(CarrinhoView, self).post(request, *args, **kwargs)
