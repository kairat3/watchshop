from django.urls import path
from like.views import LikeListView, LikeCreateView

urlpatterns = [
    path('likes/', LikeListView.as_view()),
    path('likes/create/', LikeCreateView.as_view()),
    ]
