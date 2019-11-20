from django.urls import path

from core.views import HomeView, ProductView, signup, pesquisar, CarrinhoView, CartView, remover_produto, \
    limpar_carrinho, ProfileView, category

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('accounts/signup/', signup, name='signup'),
    path('pesquisar/', pesquisar, name='search'),
    path('produtos/<int:pk>/', category, name='category'),
    path('cart/<int:pk>/', CarrinhoView.as_view(), name='add_carrinho'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:pk>', remover_produto, name='remove'),
    path('cart/clean', limpar_carrinho, name='clean'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),

]
