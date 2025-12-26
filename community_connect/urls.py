from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView

schema_view = get_schema_view(
   openapi.Info(
      title="Community Connect API",
      default_version='v1',
      description="API documentation for Community Connect",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API apps
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('opportunities.urls')),
    path('api/', include('applications.urls')),
    path('api/', include('notifications.urls')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redirect root URL to Swagger
    path('', RedirectView.as_view(pattern_name='schema-swagger-ui', permanent=False)),
]
