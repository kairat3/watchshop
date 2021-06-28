from django.urls import path
from . import views
# urlpatterns = [
#     path('', views.ProductListView.as_view()),
#     path('<int:pk>/', views.ProductDetailView.as_view()),
#     path('delete/<int:pk>/', views.ProductDeleteView.as_view()),
#     path('update/<int:pk>/', views.ProductUpdateView.as_view()),
# ]

urlpatterns = [
    path('favorites/', views.FavoriteListView.as_view()),
    path('bag/', views.BagListView.as_view()),

]
