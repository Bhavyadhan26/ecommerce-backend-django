from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('products/', views.products),
    path('add-to-cart/', views.add_to_cart),
    path('checkout/', views.checkout),
    path('cart/', views.view_cart),
    path('orders/', views.view_orders),
    

]
