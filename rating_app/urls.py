from django.urls import path
from .views import ShowRating, CreateRating, ChooseMovie

app_name = 'rating_app'

urlpatterns = [
    path('rating', ShowRating.as_view(), name='rating_page'),
    path('rating/create', CreateRating.as_view(), name='create_page'),
    path('rating/choose', ChooseMovie.as_view(), name='choose_page')
]