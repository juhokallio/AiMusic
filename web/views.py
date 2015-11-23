from django.shortcuts import render
from web.models import Composer, Composition
from composer.composer import compose_music


def training(request):
    return render(request, 'web/training.html')


def main(request):
    bach_jr = Composer.objects.get(pk=1)
    return render(request, 'web/main.html', {
        'composer': bach_jr
    })


def compose(request, composer_id):
    composer = Composer.objects.get(pk=composer_id)
    music_concepts = composer.musicconcept_set.all()
    music = compose_music(100, music_concepts)
    composition = Composition(composer, "this needs development", music)
    composition.save()
    return "ready"
