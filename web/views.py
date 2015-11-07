from django.shortcuts import render


def training(request):
    return render(request, 'web/training.html')