from django.contrib import admin
from django.urls import path, include
from myapp import url as ien_url
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('api/', include(ien_url)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
