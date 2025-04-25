from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('HOME.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
