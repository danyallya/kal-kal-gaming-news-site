from django.shortcuts import render
from django.shortcuts import render_to_response


def home(request):
    return render(request, 'home.html', {})


def main(request):
    return render_to_response('main.html')


def login(request):
    return render_to_response('login.html')


def base_game(request):
    return render_to_response('base_game.html')


def game_page(request):
    return render_to_response('game_page.html')


def profile_page(request):
    return render_to_response('profile_page.html')


def profiles_page(request):
    return render_to_response('profiles_page.html')


def profiles_pages(request):
    return render_to_response('profiles_pages.html')