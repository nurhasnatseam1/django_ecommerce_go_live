from django.urls import path ,include
from .views import (ImprovedLoginView,RegisterView,OldLoginView,ActivateAccountView,OldLoginView,RegisterView,login_page,AccountHomeView,register_page,guest_login_view)
from django.contrib.auth.views import LogoutView



app_name='accounts'




urlpatterns=[
      path("activate_email/<slug:key>/",ActivateAccountView.as_view(),name='activate_email'),
      path("resend_activate_email/",ActivateAccountView.as_view(),name='resend_activate_email'),
      path("login/",ImprovedLoginView.as_view(),name='login'),
      path("logout/",LogoutView.as_view(),name='logout'),
      path("guest_login/",guest_login_view,name='guest_login'),
      path("register/",RegisterView.as_view(),name='register'),
      path("",AccountHomeView.as_view(),name='home'),
]