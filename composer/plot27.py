__author__ = 'juho'
# Problems with Matplotlib and 3.4

from composer import tokenize, get_classic, extract_notes
from music import extract_graph, create_hc, bn_listing
import networkx as nx
import pylab as plt

#m = tokenize()[:80]
m = extract_notes(get_classic())[:80]
G = extract_graph(m)
nx.draw_networkx(G, with_labels=True)
plt.show()
print create_hc(G)
bns = bn_listing(m)[:10]
score = sum([s for s, ds in bns])
print bns
print score