from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import ListView, FormView, TemplateView

from .models import Wish
from .forms import AddForm
from rating_app.models import Movie
from rating_app.decorators import rate_film_required
from rating_app.utils import get_film_by_id, FILM, get_films_data


# Create your views here.

@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class ShowWishlist(ListView):
    model = Wish
    template_name = 'wishlist.html'

    def get_queryset(self):
        user = self.request.user
        return Wish.objects.filter(wish_user=user)

    def post(self, request):
        kp_id: int = int(request.POST['film'])
        rating: float = float(request.POST['rating'])
        film: FILM = get_film_by_id(kp_id)

        with transaction.atomic():
            Wish.objects.filter(kp_id=kp_id).delete()
            Movie.objects.create(title=film.ru_name, year=film.year, link=film.year, kp_rating=film.kp_rate,
                                 rating=rating, movie_user=request.user)

        return HttpResponseRedirect(reverse_lazy('wishlists:list_page'))


@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class AddMovie(FormView):
    form_class = AddForm
    template_name = 'add_movie.html'

    def post(self, request, *args, **kwargs):
        title: str = request.POST['title']
        return HttpResponseRedirect(reverse_lazy('wishlists:choose_page') + f'?title={title}')


@method_decorator(rate_film_required, name='dispatch')
@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class ChooseMovie(TemplateView):
    template_name = 'select_movie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title: str = self.request.GET.get('title')
        context['films_data'] = get_films_data(title)
        return context

    def post(self, request, *args, **kwargs):
        movie_id: int = int(request.POST.get('film'))
        movie_data: FILM = get_film_by_id(movie_id)
        user: str = request.user
        Wish.objects.create(kp_id=movie_id, poster=movie_data.poster_preview, title=movie_data.ru_name,
                            year=movie_data.year, link=movie_data.kp_url,
                            kp_rating=movie_data.kp_rate, wish_user=user)
        return HttpResponseRedirect(reverse_lazy('index_page'))
