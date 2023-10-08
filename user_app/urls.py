from django.urls import path
from .views import RegisterUser, LoginUser, LogoutUser

app_name = 'user_app'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_page'),
    path('login/', LoginUser.as_view(), name='login_page'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
