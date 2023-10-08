from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView,FormView

from .decorators import rate_film_required

from .models import Movie
from .forms import CreationForm
from .utils import get_films_data, get_film_by_id, FILM


class StartPage(TemplateView):
    template_name = 'index.html'


@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class ShowRating(ListView):
    model = Movie
    template_name = 'marks.html'

    def get_queryset(self):
        user = self.request.user
        ordering = self.request.GET.get('order', 'title')
        return Movie.objects.filter(movie_user=user).order_by(ordering)


    def post(self, request):
        movie_id: int = int(request.POST['film'])
        new_rating: float = float(request.POST['new_rating'])
        Movie.objects.get(pk=movie_id).update(rating=new_rating)
        return HttpResponseRedirect(reverse_lazy('movies:rating_page'))


class CreateRating(FormView):
    template_name = 'create_mark.html'
    form_class = CreationForm

    def post(self, request, *args, **kwargs):
        title: str = request.POST['title']
        rating: str = request.POST['rating']
        return HttpResponseRedirect(reverse_lazy('movies:choose_page') + f'?title={title}&rating={rating}')


@method_decorator(rate_film_required, name='dispatch')
@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class ChooseMovie(TemplateView):
    template_name = 'choose_movie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating: str = self.request.GET.get('rating')
        title: str = self.request.GET.get('title')
        context['films_data'] = get_films_data(title)
        context['rating'] = rating
        return context

    def post(self, request, *args, **kwargs):
        rating: float = float(request.POST.get('rating'))
        movie_id: int = int(request.POST.get('film'))
        movie_data: FILM = get_film_by_id(movie_id)
        user: str = request.user
        Movie.objects.create(title=movie_data.ru_name, year=movie_data.year, link=movie_data.kp_url,
                             kp_rating=movie_data.kp_rate,
                             rating=rating, movie_user=user)
        return HttpResponseRedirect(reverse_lazy('index_page'))