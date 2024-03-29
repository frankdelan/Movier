"""movie_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from user_app import views as user_views
from rating_app import views as rating_views

from rating_app.views import StartPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPage.as_view(), name='index_page'),
    path('chat/', include('chat_app.urls', namespace='chat')),
    path('users/', include('user_app.urls', namespace='users')),
    path('movies/', include('rating_app.urls', namespace='movies')),
    path('wishlist/', include('wishlist_app.urls', namespace='wishlists'))
]

