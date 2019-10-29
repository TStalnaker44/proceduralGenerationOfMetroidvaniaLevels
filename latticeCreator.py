
import random
import networkx as nx
import matplotlib.pyplot as plt

def r():
    return random.random() > dropout

def detConnection(i, node):
    if not node in completedNodes:
        if r():
            g.add_edge(i, node)
            if node not in nodes:
                nodeStack.append(node)
                nodes.append(node)

m = 5
n = 4

dropout = .4

nodeStack = []
nodes = []
completedNodes = []

g = nx.Graph()

nodeStack.append(1)

while len(nodeStack) > 0:

    i = nodeStack.pop()

    # i is in the middle of the grid
    if (n+2) <= i <= ((m-2)*n) + (n-1):

        detConnection(i, i-n)
        detConnection(i, i-1)
        detConnection(i, i+1)
        detConnection(i, i+n)
        
    # i is on the top edge
    elif 2 <= i <= n-1:

        detConnection(i, i-1)
        detConnection(i, i+1)
        detConnection(i, i+n)
        
    # i is on the bottom edge
    elif (m-1)+2 <= i <= ((m-1)*n) + (n-1):

        detConnection(i, i-n)
        detConnection(i, i-1)
        detConnection(i, i+1)
        
    # i is on the left edge
    elif i % n == 1 and (i != 1 and i != (((m-1)*n)+1)):

        detConnection(i, i-n)
        detConnection(i, i+1)
        detConnection(i, i+n)
        
    # i is on the right edge
    elif i % n == 0 and (i != n and i != m*n):

        detConnection(i, i-n)
        detConnection(i, i-1)
        detConnection(i, i+n)
        
    # i is on the top-left corner
    elif i == 1:

        detConnection(i, i+1)
        detConnection(i, i+n)
        
    # i is on the top-right corner
    elif i == n:

        detConnection(i, i-1)
        detConnection(i, i+n)
        
    # i is on the bottom-left corner
    elif i == (m-1) + 1:

        detConnection(i, i-n)
        detConnection(i, i+1)
        
    # i is on the bottom-right corner
    elif i == m*n:

        detConnection(i, i-n)
        detConnection(i, i-1)

print(nodes)

#Display the graph
pos = nx.spring_layout(g)
nx.draw_planar(g, with_labels=True, font_weight='bold')
#edge_labels = nx.get_edge_attributes(g,'object')
#nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
plt.show()
        
