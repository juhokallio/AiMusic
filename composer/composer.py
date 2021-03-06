__author__ = 'juho'

import re
import json
import random
import numpy as np
from . critic import classify
from . mlmodels import MarkovChain
from . music import Motif, extract_features, Variation, extract_notes, total_bn_score
from subprocess import call
from deap import algorithms, base, creator, tools


BACH_FILE = "data/bach"
RATINGS_FILE = "data/ratings"
CRITIC_FILE = "data/critic"
LILYPOND_OUTPUT_FILE = "music.ly"
MIDI_OUTPUT_FILE = "music.midi"


def tokenize(f_name="bach"):
    music = []
    last_length = None
    for line in open("data/" + f_name):
        line = line.replace("\n", "")
        for token in line.split(" "):
            parts = re.findall('\d+|\D+', token)
            pitch = parts[0]
            length = parts[1] if len(parts) > 1 else last_length
            last_length = length
            music.append((pitch, length))
    return music


def generate(note_count):
    mc_pitch, mc_length = bach_mcs()
    new_pitches = mc_pitch.generate(note_count, 4)
    new_lengths = mc_length.generate(note_count, 3)
    return [(new_pitches[i], new_lengths[i]) for i in range(note_count)]


def lilypondify(notes):
    output = ("\score {"
              "<<"
              "{ \key c \major ")
    for pitch, length in notes:
        output += pitch + str(int(length)) + " "
    output += ("}"
               ">>"
               "\midi { }"
               "\layout { }"
               "}")
    return output


def save_to_midi(notes):
    f = open(LILYPOND_OUTPUT_FILE, "w")

    f.write(lilypondify(notes))
    f.close()
    call("lilypond " + LILYPOND_OUTPUT_FILE, shell=True)


def play_midi():
        call("timidity " + MIDI_OUTPUT_FILE, shell=True)


def compose_to_file(length):
    music = generate(length)
    notes = extract_notes(music)
    save_to_midi(notes)


def bach_mcs():
    pitches = []
    lengths = []
    for pitch, length in tokenize():
        pitches.append(pitch)
        lengths.append(length)
    return MarkovChain(pitches, 4), MarkovChain(lengths, 4)


def jsonify(music):
    # TODO: other types
    return [{"notes": el.notes, "type": "motif"} for el in music]


def extract_music(json_o):
    music = []
    for el in json_o:
        if el["type"] == "motif":
            music.append(Motif(el["notes"]))
    return music


def extract_training(type):
    y = []
    x = []
    weights = []
    with open(RATINGS_FILE) as f:
        for line in f:
            o = json.loads(line)
            ratings = o["rating"]
            if type in ratings:
                music = extract_music(o["music"])
                x.append(extract_features(music))
                rating = int(ratings[type])
                y.append(0 if rating < 3 else 1)
                if rating == 1 or rating == 5:
                    weights.append(1)
                elif rating == 3:
                    weights.append(0.1)
                else:
                    weights.append(0.4)
    return x, y, weights


def save_rating(music, rating):
    with open(RATINGS_FILE, "a") as f:
        json.dump({
            "music": jsonify(music),
            "rating": rating
        }, f)
        f.write('\n')


def save_critic(music_index, critic):
    print("hmm")
    with open(CRITIC_FILE, "a") as f:
        json.dump(critic, f)
        f.write('\n')


def musicify(json):
    music = []
    for el in json:
        if el.type == "motif":
            music.append(Motif(el.notes))


def random_motif(mc_pitch, mc_length):
    length = random.randint(2, 8)
    pitch_order = random.randint(2, 4)
    rythm_order = random.randint(2, 4)
    pitches = mc_pitch.generate(length, pitch_order)
    lengths = mc_length.generate(length, rythm_order)
    return Motif([(pitches[i], lengths[i]) for i in range(length)])


def compose_music(target_length, critic_clfs):
    """ Compose piece of music
    This slightly hairy piece of genetic algorithm creates the music.

    target_length   Note count that is the target length. The further the music is from this length, the bigger the
                    penalty for the individual
    clf_types       List of strings that are the names of the feedback categories. Classifiers are going to be formed
                    based on these. These should come from data/ratings json, specifically from the ratings values
                    there.
    """

    # Markov chains
    mc_pitch, mc_length = bach_mcs()

    def eval(individual):
        notes = extract_notes(individual)
        """
        x = [extract_features(individual)]

        clf_p = 1
        for t in clf_types:
            clf_p *= clfs[t].predict_proba(x)[0][0]
        """
        """
        last_pitch = None
        log_likelihood = 0
        for pitch, _ in notes:
            if last_pitch is not None:
                log_likelihood += mc_pitch.log_likelihood([last_pitch, pitch])
            last_pitch = pitch



        """
        critic_factor = sum([classify(critic_clfs[t], notes) for t in critic_clfs])
        bn_score = total_bn_score(notes)
        length_penalty = abs(len(notes) - target_length) / target_length
        if bn_score == 0 or length_penalty == 1:
            return -999999.0,
        return np.log(bn_score) + critic_factor / 10 + np.log(1 - length_penalty),

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register('random_music', random_motif, mc_pitch, mc_length)

    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_music, n=1)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval)

    def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
        return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

    toolbox.register("select", selElitistAndTournament, frac_elitist=0.05, tournsize=3)

    def onePointSafe(ind1, ind2):
        size = min(len(ind1), len(ind2))
        if size > 1:
            cxpoint = random.randint(1, size - 1)
            ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
        return ind1, ind2

    toolbox.register("mate", onePointSafe)

    # Couple good ways to mutate.
    # 1. variate the parts in different ways
    # 2. add parts
    # 3. remove parts
    def mutate(individual):
        def variate():
            i = random.randint(0, len(individual) - 1)
            type = Variation.randomtype()
            individual[i] = Variation(individual[i], type)

        def add():
            r = random.random()
            if r < 0.2:
                i = random.randint(0, len(individual) - 1)
                individual.append(Motif(individual[i].notes))
            else:
                # TODO: maybe something finer than random motif, at least some of the time
                individual.append(random_motif(mc_pitch, mc_length))

        def remove():
            if len(individual) > 1:
                i = random.randint(0, len(individual) - 1)
                del individual[i]

        r = random.random()
        if r < 0.5:
            variate()
        elif r < 0.9:
            add()
        else:
            remove()

        return individual,

    toolbox.register("mutate", mutate)

    generations = 5

    pop = toolbox.population(n=40)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    crossover_prob = 0.6
    mutation_prob = 0.4

    algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, generations, stats, halloffame=hof)

    print(hof[0], eval(hof[0]))
    return hof[0]


def get_feedback_types():
    types = set()
    with open(RATINGS_FILE) as f:
        for line in f:
            o = json.loads(line)
            types.update(o["rating"].keys())
    return list(types)


def get_classic():
    """Finds and plays a piece from history (data/ratings file) that has the highest general rating
    """
    best = 0
    music = None
    with open(RATINGS_FILE) as f:
        for line in f:
            o = json.loads(line)
            ratings = o["rating"]
            if "general" in ratings:
                general = int(ratings["general"])
                if general > best:
                    music = extract_music(o["music"])
                    best = general
    return music


def get_composition(index):
    i = 0
    with open(RATINGS_FILE) as f:
        for line in f:
            i += 1
            if i == int(index):
                o = json.loads(line)
                return extract_music(o["music"])
    return None
