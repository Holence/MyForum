"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home_view, markdown_uploader

from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    path('', home_view, name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('article/', include("articles.urls")),
    path('account/', include("accounts.urls")),
    path('comment/', include("comments.urls")),
    path('messenger/', include("messenger.urls")),
    path('information/', include("informations.urls")),
    
    # 'martor/uploader/'得放在'martor/'的前面，优先级要高于martor内部设定的martor/uploader/的markdown_uploader函数
    path('martor/uploader/', markdown_uploader, name="markdown_uploader_page"),
    path('martor/', include('martor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
