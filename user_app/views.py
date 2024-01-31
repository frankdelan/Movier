from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import auth
from django.views import View
from django.views.generic import CreateView, FormView

from .forms import RegisterForm, LoginForm


# Create your views here.
class RegisterUser(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user_app:login_page')


class LoginUser(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index_page')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username: str = request.POST['username']
            password: str = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse_lazy('index_page'))
        return self.form_invalid(form)

class LogoutUser(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse_lazy('index_page'))
