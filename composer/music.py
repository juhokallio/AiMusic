__author__ = 'juho'

import random, math
import networkx as nx


class Motif:
    def __init__(self, notes):
        self.notes = notes


def elision(element):
    if len(element.notes) > 2:
        i = random.randint(0, len(element.notes) - 1)
        del element.notes[i]
    return element.notes


def change_lengths(element, changer):
    slowed_notes = []
    for pitch, length in element.notes:
        slowed_notes.append((pitch, changer(int(length))))
    return slowed_notes


def breathing(element):
    breathed = []
    for pitch, length in element.notes:
        breathed.append((pitch, length))
        breathed.append(("r", length))
    return breathed


VARIATION_TYPES = {
    "augmentation": lambda el: change_lengths(el, lambda l: l / 2),
    "diminution": lambda el: change_lengths(el, lambda l: l * 2),
    "breathing": breathing,
    "elision": elision,
    "retrograde": lambda el: el.notes[::-1]
}


class Variation:

    def __init__(self, music, type):
        self.origin = music
        self.type = type
        self.notes = VARIATION_TYPES[type](music)

    @staticmethod
    def randomtype():
        return random.choice(list(VARIATION_TYPES))



heights = {
    "c": 0,
    "his": 0,
    "des": 0.5,
    "cis": 0.5,
    "d": 1,
    "dis": 1.5,
    "es": 1.5,
    "e": 2,
    "fes": 2,
    "eis": 2.5,
    "f": 2.5,
    "fis": 3,
    "ges": 3,
    "g": 3.5,
    "gis": 4,
    "aes": 4,
    "a": 4.5,
    "ais": 5,
    "bes": 5,
    "b": 5.5
}


def numeric_height(pitch):
    octaves_to_raise = 0
    for i in range(len(pitch)):
        if pitch[-i] == "'":
            octaves_to_raise += 1
        if pitch[-i] == ",":
            octaves_to_raise -= 1
    base = pitch if octaves_to_raise == 0 else pitch[0:-octaves_to_raise]
    if base in heights:
        return heights[base] + 6 * octaves_to_raise


def pitch_movement_count(notes, change):
    count = 0
    last = None
    for pitch, length in notes:
        height = numeric_height(pitch)
        if height is not None:
            if last is not None and last - height == change:
                count += 1
            last = height
    return count


def extract_notes(music):
    notes = []
    for el in music:
        notes.extend(el.notes)
    return notes

def speed(notes):
    return sum([int(length) for pitch, length in notes]) / len(notes)


def last_note(notes):
    for note in reversed(notes):
        if note[0] != "r":
            return note

def first_note(notes):
    for note in notes:
        if note[0] != "r":
            return note


def extract_graph(notes):
    G = nx.Graph()
    for index, note in enumerate(notes):
        pitch, length = note
        length = "L" + length
        G.add_node(index)
        G.add_node(pitch)
        G.add_node(length)
        G.add_edge(pitch, index)
        G.add_edge(length, index)
        if index > 0:
            G.add_edge(pitch, index - 1)
            G.add_edge(length, index - 1)
            G.add_edge(index, index - 1)
    G.add_edge(0, len(notes) - 1)
    return G


def end_start_height_diff(notes):
    first = first_note(notes)
    if first is None:
        return 0
    return numeric_height(first[0]) - numeric_height(last_note(notes)[0])


def note_rythm(notes, fraction):
    pos = 0
    hits = 0
    count = 0
    for pitch, length in notes:
        if length == 0:
            continue
        note_length = fraction / float(length)
        if pos % 1 == 0:
            hits += 1
        if math.floor(pos) != math.floor(pos + note_length):
            count += 1
        pos += note_length
    if count == 0:
        return 0
    else:
        return hits / count


def extract_features(music):
    features = []
    notes = extract_notes(music)
    features.append(len(music))
    features.append(len(notes))
    features.extend([pitch_movement_count(notes, i) / len(notes) for i in range(-5, 5)])
    features.append(end_start_height_diff(notes))
    features.append(speed(notes))
    features.append(0 if notes[-1][0] == "r" else 1)
    features.append(sum([1 for n in notes if n[0] == "r"]) / len(notes))
    features.append(note_rythm(notes, 32))
    features.append(note_rythm(notes, 16))
    features.append(note_rythm(notes, 8))
    features.append(note_rythm(notes, 4))
    features.append(note_rythm(notes, 2))
    features.append(note_rythm(notes, 1))

    return features
