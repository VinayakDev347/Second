from django.contrib import admin
from django.urls import path, include
import frontend.urls
import backend.urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(frontend.urls)),
    path('backend/', include(backend.urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
