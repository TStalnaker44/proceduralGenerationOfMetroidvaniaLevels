
import random, grapher
import networkx as nx
import matplotlib.pyplot as plt

m = 5
n = 4

dropout = 0.4

ordering = {"red":["green","blue","orange"],
                "blue":"yellow","yellow":["brown","tan"],"brown":["pink", "purple"]}
gates = grapher.getGateOrder(ordering)

# Create keys for each gate
keys = {gate:0 for gate in gates}

def r():
    return random.random() > dropout

def detConnection(g, i, node, nodes, nodeStack, completedNodes):
    if not node in completedNodes:
        gateTech = gates[random.randint(0,len(gates)-1)]
        if i == m*n or node == m*n:
            gateTech = gates[-1]
        if r():
            g.add_edge(i, node, object=gateTech)
            if node not in nodes:
                nodeStack.append(node)
                nodes.append(node)

def createGraph():
    
    g = nx.Graph()

    nodeStack = []
    nodes = []
    completedNodes = []
    
    nodeStack.append(1)

    while len(nodeStack) > 0:

        i = nodeStack.pop()

        # i is in the middle of the grid
        if (n+2) <= i <= ((m-2)*n) + (n-1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the top edge
        elif 2 <= i <= n-1:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the bottom edge
        elif (m-1)+2 <= i <= ((m-1)*n) + (n-1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            
        # i is on the left edge
        elif i % n == 1 and (i != 1 and i != (((m-1)*n)+1)):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the right edge
        elif i % n == 0 and (i != n and i != m*n):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the top-left corner
        elif i == 1:

            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the top-right corner
        elif i == n:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes)
            
        # i is on the bottom-left corner
        elif i == (m-1) + 1:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes)
            
        # i is on the bottom-right corner
        elif i == m*n:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes)
            
    return g

g = createGraph()
while m*n not in g:
    g = createGraph()

print(gates)

#Display the graph
pos = nx.spring_layout(g)
#nx.draw_planar(g, with_labels=True, font_weight='bold')
nx.draw(g, pos, with_labels=True, font_weight='bold')
edge_labels = nx.get_edge_attributes(g,'object')
nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
plt.show()
        
