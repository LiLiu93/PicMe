"""picme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from posts import views as posts_view

urlpatterns = [
    url(r'^$', posts_view.show_post_list, name='posts_index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^accounts/', include('chat.urls')),
    url(r'^base/', include('base.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^address/', include('address.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^dialogs/', include('private_chat.urls', namespace="private_chat")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
