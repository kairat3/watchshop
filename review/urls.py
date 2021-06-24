from django.urls import path
from review.views import ReviewListCreateView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view())
    ]

