import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView

from accounts.models import Perfil
from core.forms import UserCreateForm, PerfilForm
from core.models import Produto, Categoria, Carrinho, Relatorio


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


def category(request, pk):

    categoria = Categoria.objects.get(pk=pk)
    produtos = Produto.objects.filter(categoria=categoria)

    paginator = Paginator(produtos, 5)
    page = request.GET.get('page')
    try:
        search = paginator.page(page)
    except PageNotAnInteger:
        search = paginator.page(1)
    except EmptyPage:
        search = paginator.page(paginator.num_pages)
    context = {
        'produto': produtos,
        'category': categoria
    }

    return render(request, 'produtos/categoria.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Obrigado por se registrar. Agora você está logado.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            if form.is_valid():
                Perfil.objects.create(account=new_user)
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
            try:
                carrinho = Carrinho.objects.get(cliente=user, aberto=True)
            except Carrinho.DoesNotExist:
                carrinho = Carrinho.objects.create(cliente=user, aberto=True)
            carrinho.produtos.add(produto)
            carrinho.valor += produto.preco
            carrinho.save()
            return HttpResponseRedirect(reverse('index'))
        return super(CarrinhoView, self).post(request, *args, **kwargs)


class CartView(TemplateView, LoginRequiredMixin):
    model = Produto
    template_name = 'produtos/cart.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('entrar'))
        return super().dispatch(request, *args, **kwargs)

    def soma_precos(self):
        user = self.request.user
        carrinho = Carrinho.objects.get(cliente=user, aberto=True)
        soma = 0
        for p in carrinho.produtos.all():
            soma += p.preco
        return soma

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        carrinho = Carrinho.objects.get(cliente=self.request.user, aberto=True)
        context['carrinho_checkout'] = carrinho.produtos.all()
        context['carrinho_soma'] = self.soma_precos
        return context


def remover_produto(request, pk):
    if request.user.is_authenticated:
        produto = get_object_or_404(Produto, pk=pk)
        user = request.user
        carrinho = Carrinho.objects.get(cliente=user, aberto=True)
        carrinho.save()
        carrinho.produtos.remove(produto)
    return HttpResponseRedirect(reverse('cart'))


def today():
    return datetime.date.today()


def limpar_carrinho(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            cart = Carrinho.objects.get(cliente=user, aberto=True)
            try:
                r = Relatorio.objects.get(mes=today().month, ano=today().year)
                r.valor += cart.valor
                r.save()
                cart.aberto = False
                cart.save()
                Carrinho.objects.create(cliente=user)
            except Relatorio.DoesNotExist:
                Relatorio.objects.create(titulo='Relatório %s/%s' % (cart.data.month, cart.data.year), mes=cart.data.month, ano=cart.data.year, valor=cart.valor)
                cart.aberto = False
                cart.save()
                Carrinho.objects.create(cliente=user)
        except Carrinho.DoesNotExist:
            Carrinho.objects.create(cliente=user)
        return HttpResponseRedirect(reverse('cart'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'produtos/profile.html'

    def get_success_url(self):
        perfil = Perfil.objects.get(account=self.request.user)
        return reverse_lazy('profile', kwargs={'pk': perfil.id})
