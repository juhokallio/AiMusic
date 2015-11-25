__author__ = 'juho'
from composer import tokenize
from music import extract_graph
import networkx as nx
import pylab as plt

m = tokenize()
G = extract_graph(m[:10])
nx.draw_networkx(G, with_labels=True)
plt.show()