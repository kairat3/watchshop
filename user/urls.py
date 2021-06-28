from django.urls import path
from user.views import RegisterApiView, LoginApiView, ActivationView, PassResetApiView, NewPasswordApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view(), name='activate_account'),
    path('pass_reset/', PassResetApiView.as_view()),
    path('new_password/', NewPasswordApiView.as_view()),
]