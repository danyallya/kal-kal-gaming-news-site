from django.shortcuts import render
from django.shortcuts import render_to_response


def home(request):
    return render(request, 'home.html', {})


def main(request):
    return render_to_response('main.html')