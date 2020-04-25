from django.urls import path


from .views import (ProductListView,ProductDetailView,
                        ProductFeaturedListView,
                        ProductFeaturedDetailView,

                        )




app_name="products"



urlpatterns=[
      path("",ProductListView.as_view(),name="list"),
      path("<slug:slug>/",ProductDetailView.as_view(),name='detail'),
      path('featured/',ProductFeaturedListView.as_view(),name='featured-list'),
      path('featured/<int:pk>/',ProductFeaturedDetailView.as_view(),name="featured-detail"),
]