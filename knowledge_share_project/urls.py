"""knowledge_share_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from rango import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rango/', include('rango.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^rango/register/$', views.RangoRegistrationView.as_view(), name='registration_register'),
    # 这两个rango/register以前是accounts/register
    re_path(r'^rango/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)