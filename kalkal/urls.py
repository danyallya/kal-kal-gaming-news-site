"""fanoos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url, handler404
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),  # admin site

]

if settings.ENABLE_SITE:
    urlpatterns += [
        # url(r'^account/', include('account.urls')),


        url(r'^faq/$', 'account.views.faq', name='faq'),

    ]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += [
    url(r'^select2/', include('django_select2.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

# handler404 = 'movie.views.handler404'
