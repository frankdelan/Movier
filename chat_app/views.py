from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


# Create your views here.
@method_decorator(login_required(login_url='users:login_page'), name='dispatch')
class ChatPage(TemplateView):
    template_name = 'chat_app/index.html'
