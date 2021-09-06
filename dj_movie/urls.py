"""dj_movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    #  добавляем путь для преключения языков
    path('i18n/', include('django.conf.urls.i18n')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]


# и так же создаем раздел urlpatterns для указания на каких страницах делать переводить наш текст
urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    # в моем случае это:
    # 1) контакты
    path('contact/', include('contact.urls')),
    # 2) наши фильмы
    path('', include('movies.urls')),  # регестрируем файл урл в дир мувис

)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
