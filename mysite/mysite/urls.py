from django.contrib import admin
from django.urls import path,include
from blog import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls', namespace='blog')),
    path('social/',include('social_django.urls', namespace='social')),
    path('account/',include('account.urls')),
    path('summmernote/',include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
