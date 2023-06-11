from django.shortcuts import render
from .forms import SimpleMessageForm

def index(request):
    return render(request, 'chat/index.html', {
        'form': SimpleMessageForm(),
    })