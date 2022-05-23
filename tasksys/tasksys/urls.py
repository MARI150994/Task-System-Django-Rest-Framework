from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[path('api/task/', include('task.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger-ui/', TemplateView.as_view(
        template_name='swaggerui/swaggerui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/task/', include('task.urls')),
    path('api/company/', include('my_auth.urls')),
]
