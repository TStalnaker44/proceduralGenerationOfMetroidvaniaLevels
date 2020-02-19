
import networkx as nx
import random
import matplotlib.pyplot as plt

def tester():
    # Create a linear graph
    ordering = ["red","green","blue","orange","pink"]
    g = createGraph(dictFromList(ordering))
    plot(g)

    # Create a branching graph
##    ordering = {"red":["green","blue","purple"],"green":"orange",
##                "blue":"black","black":["pink","yellow","brown"],
##                "brown":"white"}
    #ordering = {"neutral":"grey","grey":["red","orange"],"red":"green","green":"blue",
    #           "orange":["yellow","white"],"yellow":"purple"}
    ordering = {"red":["green","purple"],"green":"blue","purple":"yellow"}

    for x in range(10):
        getGateOrder(ordering)
        
    g = createGraph(ordering)
    plot(g)



    print([x for x in nx.topological_sort(g)])

    
def plot(g):
    #Display the graph
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, font_weight='bold')
    edge_labels = nx.get_edge_attributes(g,'object')
    nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
    plt.show()

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
    
    # Improve this with a better solution
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
            
            

if __name__ == "__main__":
    tester()
