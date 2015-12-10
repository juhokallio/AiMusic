__author__ = 'juho'
# Problems with Matplotlib and 3.4

from composer.composer import tokenize, get_classic, extract_notes, save_to_midi, play_midi, get_composition
from composer.music import extract_graph, create_hc, bn_listing
import networkx as nx
import pylab as plt

notes = tokenize("bwv772inventio1")

#notes = []
"""
for i in range(22, 24):
    m = get_composition(i)
    notes.extend(extract_notes(m))
"""
#notes = extract_notes(get_composition(27))
#save_to_midi(notes)
#play_midi()
#m = extract_notes(get_classic())[:15]


print(len(notes))
G = extract_graph(notes)
nx.draw_networkx(G, with_labels=True)
plt.show()
print create_hc(G)
bns = bn_listing(notes)
print bns
print "best", bns[0][0]
print "top 10", sum([s for s, ds in bns[:10]])
print "all", sum([s for s, ds in bns])
