
import networkx as nx
import random
import matplotlib.pyplot as plt
    
def dictFromList(lyst):
    d = {}
    for x in range(1, len(lyst)):
        d[lyst[x-1]] = lyst[x]
    return d
        
def createGraph(gates):

    g = nx.DiGraph()

    for key in gates:
        if type(gates[key]) == list:
            for gate in gates[key]:
                g.add_edge(key, gate)
        else:
            g.add_edge(key, gates[key])
    return g

def getGateOrder(ordering):
    """Function that creates a viable ordering for the
    provided keys given their ordering criteria"""
    
    # Create a graph (tree) of the gating techniques
    g = createGraph(ordering)

    # Find the start node
    start = [node for node, degree in g.in_degree() if degree==0][0]
    order, used = [start], [start]
    possibleNext = []
    
    while len(order) < g.number_of_nodes():
        for node in order:
            for x in g.neighbors(node):
                possibleNext.append(x)
        posNex = random.choice(possibleNext)
        if not posNex in order:
            order.append(posNex)
        
    return order

def getDirectionalMapping(mappings):
    ret = []
    for item in mappings:
        if type(item) == str:
            ret.append((item, item))
        elif type(item) == tuple:
            ret.append(item)
    return ret
