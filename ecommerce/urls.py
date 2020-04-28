"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import base
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from accounts.views import login_page,register_page,guest_login_view
from cart.views import cart_home
from address.views import checkout_address_create_view,checkout_address_reuse_view
from orders.views import order_sucess
urlpatterns = [
    path("",base,name='base'),
    path("login/",login_page,name='login'),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("guest_login/",guest_login_view,name='guest_login'),
    path("register/",register_page,name='register'),
    path('admin/', admin.site.urls),
    path('products/',include('products.urls')),
    path('search/',include('search.urls')),
    path('cart/',include('cart.urls')),
    path('checkout/address/create/',checkout_address_create_view,name='checkout-address'),
    path("checkout/address/reuse/",checkout_address_reuse_view,name="checkout-address-reuse"),
    path("order/success",order_sucess,name="order-success"),
]



if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)