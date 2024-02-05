from django.urls import path
from .views import ChatPage

app_name = 'chat_app'

urlpatterns = [
    path('', ChatPage.as_view(), name='chat_page'),
]