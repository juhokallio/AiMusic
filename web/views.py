from django.shortcuts import render, render_to_response
from web.models import Composer, Composition
from composer.composer import compose_music, get_composition, jsonify, save_critic
import json
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.http import JsonResponse


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def training(request, piece_id):
    music = get_composition(piece_id)
    music_json = json.dumps(jsonify(music))
    print(music_json)
    response = render_to_response("web/training.html", {
        "music": music_json,
        "id": piece_id
    }, context_instance=RequestContext(request))
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response['Pragma'] = 'no-cache'
    return response


def save_critic(request, piece_id):
    critic = request.POST['critic']
    print(critic)
    print(piece_id)
    save_critic(piece_id, critic)
    return JsonResponse()


def main(request):
    bach_jr = Composer.objects.get(pk=1)
    return render(request, "web/main.html", {
        "composer": bach_jr
    })


def compose(request, composer_id):
    composer = Composer.objects.get(pk=composer_id)
    music_concepts = composer.musicconcept_set.all()
    music = compose_music(100, music_concepts)
    composition = Composition(composer, "this needs development", music)
    composition.save()
    return "ready"
