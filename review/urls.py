from django.urls import path
from review.views import ReviewListCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),
    path('reviews/update/<int:pk>/', ReviewUpdateView.as_view()),
    path('reviews/<int:pk>/', ReviewDeleteView.as_view()),
    ]

