"""Auth_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
import Auth_app.views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', Auth_app.views.home, name = 'home'),
    url(r'^login_auth/$', Auth_app.views.login, name = 'login'),
    url(r'^portal/$', Auth_app.views.portal, name = 'portal'),
    url(r'^auth/$', Auth_app.views.auth, name = 'auth'),
    url(r'^gw_message/$', Auth_app.views.msg, name = 'msg'),
    url(r'^ping/$', Auth_app.views.ping, name = 'ping'),
    
]
