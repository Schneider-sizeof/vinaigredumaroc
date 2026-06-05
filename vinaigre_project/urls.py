from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', core_views.sitemap_xml, name='sitemap'),
    path('robots.txt', core_views.robots_txt, name='robots'),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=True
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
