
import networkx as nx
import random
import matplotlib.pyplot as plt

def tester():
    # Create a linear graph
    ordering = ["red","green","blue","orange","pink"]
    g = createGraph(dictFromList(ordering))
    plot(g)

    # Create a branching graph
    ordering = {"red":["green","blue","purple"],"green":"orange",
                "blue":"black","black":["pink","yellow","brown"],
                "brown":"white"}
    g = createGraph(ordering)
    plot(g)

    #print([x for x in nx.topological_sort(g)])

    
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
    #print(g.edges())
    return g

def getGateOrder(ordering):
    g = createGraph(ordering)
    return [x for x in nx.topological_sort(g)]

if __name__ == "__main__":
    tester()
