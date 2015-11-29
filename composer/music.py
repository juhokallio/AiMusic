__author__ = 'juho'

import random, math
import networkx as nx
import numpy as np
import unittest
from scipy.cluster import hierarchy
from scipy.spatial import distance
from collections import defaultdict


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


def get_patterns(notes, index, max_length=4):
    patterns = set()
    for pattern_length in range(min(max_length, index + 1)):
        pitches = []
        lengths = []
        # TODO: missing as well
        for i in range(max(0, index - pattern_length), index + 1):
            pitch, length = notes[i]
            pitches.append(pitch)
            lengths.append("L" + length)
        patterns.add(tuple(pitches))
        patterns.add(tuple(lengths))
    return patterns


def extract_graph(notes):
    G = nx.Graph()
    unused_patterns = {}
    used_patterns = set()
    for index, note in enumerate(notes):
        patterns = get_patterns(notes, index)
        for p in patterns:
            if p in unused_patterns:
                G.add_node(p)
                used_patterns.add(p)
                G.add_edge(index, p)
                G.add_edge(unused_patterns.pop(p), p)
            elif p in used_patterns:
                G.add_edge(index, p)
            else:
                unused_patterns[p] = index

        G.add_node(index)
        if index > 0:
            G.add_edge(index, index - 1)
    G.add_edge(0, len(notes) - 1)
    return G


def create_hc(G):
    node_idx = {}
    for i, node in enumerate(G.nodes()):
        node_idx[node] = i


    """Creates hierarchical cluster of graph G from distance matrix"""
    path_length=nx.all_pairs_shortest_path_length(G)
    distances=np.zeros((len(G),len(G)))
    for u,p in path_length.items():
        for v,d in p.items():
            distances[node_idx[u]][node_idx[v]]=d
    # Create hierarchical cluster
    Y=distance.squareform(distances)
    Z=hierarchy.complete(Y)  # Creates HC using farthest point linkage
    # This partition selection is arbitrary, for illustrive purposes
    membership=list(hierarchy.fcluster(Z,t=1.15))
    # Create collection of lists for blockmodel
    partition=defaultdict(list)
    for n_i,p in zip(list(range(len(G))),membership):
        node = G.nodes()[n_i]
        if isinstance(node, (int, long)):
            partition[p].append(node)
    return list(partition.values())


def bn(G, d1, d2):
    bns = set()
    for n in d1:
        for ne1 in nx.all_neighbors(G, n):
            if ne1 in d2:
                bns.add(n)
                bns.add(ne1)
            for ne2 in nx.all_neighbors(G, ne1):
                if ne2 in d2:
                    bns.add(ne1)
    return bns


def bn_score(G, d1, d2):
    bns = bn(G, d1, d2)
    degree_weigth = 0.5 * sum([nx.degree(G, n) for n in bns])
    balance = min(len(d1), len(d2)) / float(max(len(d1), len(d2)))
    size = len(d1) + len(d2)
    return degree_weigth * balance * size


def total_bn_score(notes):
    G = extract_graph(notes)
    nx.draw_networkx(G, with_labels=True)
    plt.show()
    bns = bn_listing(m[:100])
    # Sum of bisociation scores seems to work quite nicely.
    return sum([s for s, ds in bns])


def bn_listing(notes):
    G = extract_graph(notes)
    domains = create_hc(G)
    scores = []
    for i1 in range(len(domains)):
        for i2 in range(i1 + 1, len(domains)):
            ds = domains[i1], domains[i2]
            scores.append((bn_score(G, *ds), ds))
    scores.sort(reverse=True)
    return scores


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


class PatternExtractionTest(unittest.TestCase):
    notes = [("d", "2"), ("d", "16"), ("a", "1")]

    def testIndexZero(self):
        patterns = get_patterns(self.notes, 0)
        expected_patterns = set([("d",), ("L2",)])
        self.assertEquals(expected_patterns, patterns, msg="Wrong patterns with index 0")

    def testIndexOne(self):
        patterns = get_patterns(self.notes, 1)
        expected_patterns = set([("d",), ("d", "d"), ("L16",), ("L2", "L16")])
        self.assertEquals(expected_patterns, patterns, msg="Wrong patterns with index 1")

    def testIndexOneWithMaxLengthOne(self):
        patterns = get_patterns(self.notes, 1, max_length=1)
        expected_patterns = set([("d",), ("L16",)])
        self.assertEquals(expected_patterns, patterns, msg="Wrong max one length patterns with index 1")
