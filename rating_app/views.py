from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView,FormView

from .decorators import rate_film_required

from .models import Movie
from .forms import CreationForm, AddIdForm
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
        action = request.POST.get('action')
        if action == 'update':
            movie_id = int(request.POST.get('film'))
            new_rating = float(request.POST.get('new_rating'))
            movie = get_object_or_404(Movie, pk=movie_id)
            movie.rating = new_rating
            movie.save()
        elif action == 'delete':
            movie_id = int(request.POST.get('film'))
            movie = get_object_or_404(Movie, pk=movie_id)
            movie.delete()

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
        try:
            movie_id: int = int(request.POST.get('film'))
        except TypeError:
            return HttpResponse('<h1>Фильм с таким названием не найдем</h1>')

        movie_data: FILM = get_film_by_id(movie_id)
        user: str = request.user
        Movie.objects.create(title=movie_data.ru_name, year=movie_data.year, link=movie_data.kp_url,
                             kp_rating=movie_data.kp_rate,
                             rating=rating, movie_user=user)
        return HttpResponseRedirect(reverse_lazy('movies:rating_page'))


class AddId(FormView):
    template_name = 'add_id.html'
    form_class = AddIdForm
    success_url = 'movies:rating_page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating'] = self.request.GET.get('rating')
        return context

    def post(self, request, *args, **kwargs):
        rating: int = self.request.POST.get('rating')
        movie_id: int = self.request.POST.get('id')
        user: str = self.request.user

        try:
            movie_data: FILM = get_film_by_id(movie_id)
        except:
            return HttpResponse('<h1>Фильм с таким id не найдем</h1>')

        Movie.objects.create(title=movie_data.ru_name, year=movie_data.year, link=movie_data.kp_url,
                             kp_rating=movie_data.kp_rate,
                             rating=rating, movie_user=user)
        return HttpResponseRedirect(reverse_lazy('movies:rating_page'))

