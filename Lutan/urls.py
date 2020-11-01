"""Lutan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from djoser.conf import settings as djoser_settings
from djoser.views import TokenCreateView
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.schemas.openapi import AutoSchema

from Lutan.openapi_info import DEFAULT_INFO

"""
Use custom schema to customize djoser TokenCreateView's schema generation via monkey patch.
The reason for doing so is TokenCreateView using two different serializer class:
one is djoser_settings.SERIALIZERS.token_create for deserializing the POST request body which contains the authentication credential.
one is djoser_settings.SERIALIZERS.token for serializing the response which contains the auth_token.
The schema generation process of django rest framework depends on the serializer to determine the schema.
"""


class TokenCreateViewSchema(AutoSchema):
    def _get_request_body(self, path, method):
        self._get_serializer = lambda path, method: djoser_settings.SERIALIZERS.token_create()
        return super(TokenCreateViewSchema, self)._get_request_body(path, method)

    def _get_responses(self, path, method):
        self._get_serializer = lambda path, method: djoser_settings.SERIALIZERS.token()
        return super(TokenCreateViewSchema, self)._get_responses(path, method)


TokenCreateView.schema = TokenCreateViewSchema()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('categories.urls')),
    path('', include('threads.urls')),
    path('', include('posts.urls')),
    path('', include('avatars.urls')),
]


schema_view = get_schema_view(
    DEFAULT_INFO,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_swagger_ui_view = schema_view.with_ui('swagger', cache_timeout=0)
schema_swagger_without_ui_view = schema_view.without_ui(cache_timeout=0)

urlpatterns += [
    path('swagger/', schema_swagger_ui_view, name='schema-swagger-ui'),
    re_path('swagger(?P<format>\.json|\.yaml)$',
            schema_swagger_without_ui_view, name='schema-swagger-without-ui')
]
