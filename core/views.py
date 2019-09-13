from django.contrib.auth import views as auth_views, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, DetailView

from core.forms import UserCreateForm
from core.models import Produto, Categoria


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


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(60 * 60 * 24 * 30)  # one month validity
    return auth_views.LoginView(request, *args, **kwargs)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'admin/signup.html', {'form': form})
