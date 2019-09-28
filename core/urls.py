from django.urls import path

from core.views import HomeView, ProductView, signup, pesquisar, CarrinhoView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('accounts/signup/', signup, name='signup'),
    path('pesquisar/', pesquisar, name='search'),
    path('cart/<int:pk>/', CarrinhoView.as_view(), name='add_carrinho'),
]
