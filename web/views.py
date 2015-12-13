from django.shortcuts import render, render_to_response, get_object_or_404
from web.models import Composer, Composition, Critic
from composer.composer import compose_music, get_composition, jsonify
import json
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def training(request, piece_id):
    composition = Composition.objects.get(id=piece_id)
    critic = composition.critics.first()
    response = render_to_response("web/training.html", {
        "music": json.dumps(composition.music),
        "critic": json.dumps(critic.critic if critic else ""),
        "id": piece_id
    }, context_instance=RequestContext(request))
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response['Pragma'] = 'no-cache'
    return response


def save_critic(request, piece_id):
    critic_json = request.POST['critic']
    composition = get_object_or_404(Composition, id=piece_id)
    critic = composition.critics.first()
    if critic is None:
        critic = Critic.objects.create(composition=composition, critic=critic_json)
    else:
        critic.critic = critic_json
    critic.save()
    return HttpResponse("ready")


def main(request):
    bach_jr = get_object_or_404(Composer, id=1)
    compositions = [{"id": c.id, "name": c.name} for c in bach_jr.compositions.all()]
    return render(request, "web/main.html", {
        "composer": bach_jr,
        "compositions": compositions
    })


def compose(request, composer_id):
    composer = Composer.objects.get(pk=composer_id)
    music_concepts = composer.musicconcept_set.all()
    music = compose_music(60, music_concepts)
    del music.fitness
    music = json.dumps(music, default=lambda o: o.__dict__)
    composition = Composition.objects.create(composer=composer, name="this needs development", music=music)
    composition.save()
    return main(request)
