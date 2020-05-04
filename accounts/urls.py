from django.urls import path ,include
from .views import (ActivateAccount,LoginView,RegisterView,login_page,AccountHomeView,register_page,guest_login_view)
from django.contrib.auth.views import LogoutView



app_name='accounts'




urlpatterns=[
      path("activate_email/<slug:key>/",ActivateAccount,name='activate_email'),
      path("login/",login_page,name='login'),
      path("logout/",LogoutView.as_view(),name='logout'),
      path("guest_login/",guest_login_view,name='guest_login'),
      path("register/",register_page,name='register'),
      path("",AccountHomeView.as_view(),name='home'),
]