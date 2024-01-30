from django.urls import path
from .views import ChooseMovie, ShowWishlist, AddMovie

app_name = 'wishlist_app'

urlpatterns = [
    path('', ShowWishlist.as_view(), name='list_page'),
    path('add/', AddMovie.as_view(), name='add_page'),
    path('choose/', ChooseMovie.as_view(), name='choose_page'),

]