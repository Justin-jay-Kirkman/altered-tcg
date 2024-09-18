from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')


def fix_deck(request):
    return render(request, 'fix_deck.html')
