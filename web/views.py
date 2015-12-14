from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from web.models import Composer, Composition, Critic, Midi
from composer.composer import compose_music, save_to_midi
from composer.music import extract_notes
import json
from composer.critic import get_classifiers
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required
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


@login_required
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


@login_required
def main(request):
    bach_jr = get_object_or_404(Composer, id=1)
    compositions = [{"id": c.id, "name": c.name} for c in bach_jr.compositions.all()]
    return render(request, "web/main.html", {
        "composer": bach_jr,
        "compositions": compositions
    })


@login_required
def compose(request, composer_id):
    composer = get_object_or_404(Composer, id=1)
    critic_clfs = get_classifiers(composer.compositions.all())
    music = compose_music(60, critic_clfs)
    del music.fitness
    notes = extract_notes(music)
    music = json.dumps(music, default=lambda o: o.__dict__)
    composition = Composition.objects.create(composer=composer, name="this needs development", music=music)
    composition.save()
    save_to_midi(notes)
    midi_to_db(composition)
    return main(request)


@login_required
def get_midi(request, composition_id):
    midi = get_object_or_404(Midi, composition_id=composition_id)
    return HttpResponse(midi.data, content_type="audio/midi")


def login_page(request):
    return render(request, "web/login.html")


def attempt_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("/")
            # Redirect to a success page.
        else:
            return login_page(request)
    else:
        return login_page(request)


def midi_to_db(composition):
    # TODO: to a variable. Also, should contain the composition id or something
    with open("music.midi", mode='rb') as file:
        midi = Midi.objects.create(composition=composition, data=file.read())
        midi.save()
