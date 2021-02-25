from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from boards import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('board/', include('boards.urls')),
    path('user/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
