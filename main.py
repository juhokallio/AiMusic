__author__ = 'juho'
from models import MarkovChain
from subprocess import call
import re


def tokenize(music_file):
    music = []
    last_length = None
    for line in open(music_file):
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


def lilypondify(music):
    output = ("\score {"
              "<<"
              "{ \key c \major ")
    for pitch, length in music:
        output += pitch + length + " "
    output += ("}"
               ">>"
               "\midi { }"
               "\layout { }"
               "}")
    return output


def save_music_to_file(music):
    f = open('music.ly', 'w')
    f.write(lilypondify(music))
    f.close()
    call("lilypond music.ly", shell=True)
    call("timidity music.midi", shell=True)


def compose_to_file(length):
    music = generate(length)
    save_music_to_file(music)


def bach_mcs():
    pitches = []
    lengths = []
    for pitch, length in tokenize("data/bach"):
        pitches.append(pitch)
        lengths.append(length)
    mc_pitch = MarkovChain(pitches, 4)
    mc_length = MarkovChain(lengths, 4)
    return mc_pitch, mc_length


mc_pitch, mc_length = bach_mcs()
#compose_to_file(300)

'''DEAP example. We try to evolve a list of digits to match a target list of
digits, that represents a date.
'''
import random
from deap import algorithms
from deap import base
import numpy as np
from deap import creator
from deap import tools
from music import Motif


# Our evaluation function
def eval(individual):
    # Evaluation function has to return a tuple, even if there is only one
    # evaluation criterion (thats why there is a comma).
    return len([1 for i in range(len(individual)) if individual[i] == target[i]]),

# We create a fitness for the individuals, because our eval-function gives us
# "better" values the closer they are zero, we will give it weight -1.0.
# This creates a class creator.FitnessMin(), that is from now on callable in the
# code. (Think about Java's factories, etc.)
creator.create("FitnessMin", base.Fitness, weights=(1.0,))

# We create a class Individual, which has base type of list, it also uses our
# just created creator.FitnessMin() class.
creator.create("Individual", list, fitness=creator.FitnessMin)

# We create DEAP's toolbox. Which will contain our mutation functions, etc.
toolbox = base.Toolbox()


def random_motif():
    length = random.randint(2, 8)
    pitch_order = random.randint(2, 4)
    rythm_order = random.randint(2, 4)
    pitches = mc_pitch.generate(length, pitch_order)
    lengths = mc_length.generate(length, rythm_order)
    return Motif([(pitches[i], lengths[i]) for i in range(length)])

m = random_motif()
save_music_to_file(m.notes)
"""
# We create a function named 'random_digit', which calls random.randint
# with fixed parameters, i.e. calling toolbox.random_digit() is the same as
# calling random.randint(0, 9)
toolbox.register('random_music', random_motif)

# Now, we can make our individual (genotype) creation code. Here we make the function to create one instance of
# creator.Individual (which has base type list), with tools.initRepeat function. tool.initRepeat
# calls our just created toolbox.random_digit function n-times, where n is the
# length of our target. This is about the same as: [random.randint(0,9) for i in xrange(len(target))].
# However, our created individual will also have fitness class attached to it (and
# possibly other things not covered in this example.)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_music, n=1)

# As we now have our individual creation code, we can create our population code
# by making a list of toolbox.individual (which we just created in last line).
# Here it is good to know, that n (population size), is not defined at this time
# (but is needed by the initRepeat-function), and can be altered when calling the
# toolbox.population. This can be achieved by something called partial functions, check
# https://docs.python.org/2/library/functools.html#functools.partial if interested.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# We register our evaluation function, which is now callable as toolbox.eval(individual).
toolbox.register("evaluate", eval)

def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
    return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

# We use simple selection strategy where we select only the best individuals,
# now callable in toolbox.select.
toolbox.register("select", selElitistAndTournament, frac_elitist=0.05 , tournsize=3)


def mate(i1, i2):
    for i in range(len(i1)):
        i1[i] = 1 if random.random() < darkness / 16.0 else 0
        i2[i] = 1 if random.random() < darkness / 16.0 else 0
    return i1, i2

# We use one point crossover, now callable in toolbox.mate.
toolbox.register("mate", mate)


# We define our own mutation function which replaces one index of an individual
# with random digit.
def mutate(individual):
    for i in range(len(individual)):
        darkness = get_darkness(individual, i)
        target = 8 - darkness if individual[i] == 1 else darkness
        if random.random() < target / 100.0:
            individual[i] = 1 - individual[i]
    # DEAP's mutation function has to return a tuple, thats why there is comma
    # after.
    return individual,

# We register our own mutation function as toolbox.mutate
toolbox.register("mutate", mutate)

# Now we have defined basic functions with which the evolution algorithm (EA) can run.
# Next, we will define some parameters that can be changed between the EA runs.

# Maximum amount of generations for this run
generations = 30

# Create population of size 100 (Now we define n, which was missing when we
# registered toolbox.population).
pop = toolbox.population(n=30)

# Create hall of fame which stores only the best individual
hof = tools.HallOfFame(1)

# Get some statistics of the evolution at run time. These will be printed to
# sys.stdout when the algorithm is running.
import numpy as np
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

# Probability for crossover
crossover_prob = 0.7

# Probability for mutation
mutation_prob = 0.2

# Call our actual evolutionary algorithm that runs the evolution.
# eaSimple needs toolbox to have 'evaluate', 'select', 'mate' and 'mutate'
# functions defined. This is the most basic evolutionary algorithm. Here, we
# have crossover probability of 0.7, and mutation probability 0.2.
algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, generations, stats, halloffame=hof)

# Print the best individual, and its fitness
print(hof[0], eval(hof[0]))

"""
