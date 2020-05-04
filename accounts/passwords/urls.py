from django.urls import path,re_path
from django.contrib.auth import views as auth_views 





#difference between change and reset is that (change) process happen only with your server's processing
#and the reset process takes user email to confirm the change

urlpatterns=[
      path('change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
      path('change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
      path('reset/',auth_views.PasswordResetView.as_view(),name='password_reset'), #sepecify new password
      path('reset/done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'), #will tell you that it has send you email with the appropriate link
      path('reset/<slug:uidb64>/<slug:token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'), #emailed link will revert you here 
      path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]


