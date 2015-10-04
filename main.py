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
    music = tokenize("data/bach")
    pitches = []
    lengths = []
    for pitch, length in music:
        pitches.append(pitch)
        lengths.append(length)
    mc_pitch = MarkovChain(pitches, 2)
    mc_length = MarkovChain(lengths, 3)
    new_pitches = mc_pitch.generate(note_count)
    new_lengths = mc_length.generate(note_count)
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


def compose_to_file(length):
    music = lilypondify(generate(length))
    f = open('music.ly', 'w')
    f.write(music)
    f.close()
    call("lilypond music.ly", shell=True)
    call("timidity music.midi", shell=True)


compose_to_file(300)
