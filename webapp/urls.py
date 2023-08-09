from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',Home.as_view(),name='home'),  
    path('products_search',Products_search.as_view(),name='products_search'),  
    path('filter_category/<str:query>',Filter_Category.as_view(),name='filter_category'),  
    path('filter_products/<str:category>',Filter_products.as_view(),name='filter_products'),  
    path('product_view/<slug>',Product_view.as_view(),name='product_view'),  
    path('get_online_quote',G_online_quote.as_view(),name='get_online_quote'),
    path('Facility',faciities.as_view(),name='Facility'),
    path('login',loginView.as_view(),name='login'),
    path('logout',logoutView.as_view(),name='logout'),
    path('about',about.as_view(),name='about'),
    path('contact',contact.as_view(),name='contact'),
    path('search',searchpage,name='search'),
    path('search/<str:name>',SearchProduct,name='search'),
    path('Searchproduct',SearchProductnoapi.as_view(),name='SearchProductnoapi'),
    path('cart',cart.as_view(),name='cart'),
    path('signup',Signupview.as_view(),name='signup'),
    path('checkout',checkOut,name='checkout'),
    path('add2cart/<slug>',add2cart,name='add2cart'),
    path('cart_items_delete/<str:pname>',cart_items_delete,name='items_delete'),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)