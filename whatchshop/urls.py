from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Watch shop API",
        default_version='v1',
        description="Welcome to the world of Watch shop",
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/', include('like.urls')),
    path('api/v1/', include('review.urls')),

]
