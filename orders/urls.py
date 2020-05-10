from django.urls import path 




from .views import (ProductDownloadView,OrderListView,OrderDetailView,order_sucess,LibraryView)




app_name='orders'



urlpatterns=[
      path('',OrderListView.as_view(),name='list'),
      path('<slug:order_id>/',OrderDetailView.as_view(),name='detail'),
      path("success/",order_sucess,name="order-success"),
      path('<slug:order_id>/<int:pk>/',ProductDownloadView.as_view(),name='download'),
]