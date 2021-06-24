
from django.contrib import admin
from django.urls import path, include
# django_likes/urls.py

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/reviews/', include('review.urls')),
    path('api/v1/likes/', include('like.urls'))
]
