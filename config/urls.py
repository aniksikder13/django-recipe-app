from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
            'api/schema/',
            SpectacularAPIView.as_view(),
            name='schema'
        ),
    # Docs UI urls:
    path(
            'api/docs/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui'
        ),
    path(
            'api/redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc'
        ),
    # Api token:
    path(
            'api/token/',
            TokenObtainPairView.as_view(),
            name='token_obtain_pair'
        ),
    path(
            'api/token/refresh/',
            TokenRefreshView.as_view(),
            name='token_refresh'
        ),
    # app urls include:
    path('api/user/', include('user.urls'))
]
