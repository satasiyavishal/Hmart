
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),
    path('',views.HOME,name='home'),
    path('products/',views.PRODUCT,name='product'),
    path('product_details/<str:id>',views.PRODUCT_DETAIL_PAGE,name='product_detail'),
    path('search/',views.SEARCH,name='search'),
    path('contact/',views.CONTACT_PAGE,name='contact'),
    path('about/',views.ABOUT_PAGE,name='about'),
    
    
    path('register/',views.HandleRegister,name='register'),
    path('login/',views.HandleLogin,name='login'),
    path('logout/',views.HandleLogout,name='logout'),


    #Cart Path
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/checkout',views.Check_out,name='checkout'),
    path('cart/checkout/placeorder',views.Place_order,name='place_order'),
    path('success/',views.SUCCESS,name='success'),
    path('Your_Order/',views.Your_Order,name='your_order'),


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
