
import random, grapher
import networkx as nx
import matplotlib.pyplot as plt

dropout = 0.4

def r():
    return random.random() > dropout

def detConnection(g, i, node, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral=0):
    if not node in completedNodes:
        
        # If the user wants more neutral connections
        if weightedNeutral != 0:
            if random.random() < weightedNeutral:
                gateTech = gates[0]
            else:
                gateTech = gates[random.randint(1,len(gates)-1)]
        else:
            gateTech = gates[random.randint(0,len(gates)-1)]
            
        if i == endNode or node == endNode:
            gateTech = gates[-1]
        if r():
            g.add_edge(i, node, object=gateTech)
            if node not in nodes:
                nodeStack.append(node)
                nodes.append(node)

def createGraph(dimensions, gates, weightedNeutral=0, endNode=None):

    m,n = dimensions

    g = nx.Graph()

    nodeStack = []
    nodes = []
    completedNodes = []
    
    nodeStack.append(1)

    while len(nodeStack) > 0:

        i = nodeStack.pop()

        # i is in the middle of the grid
        if i % n != 0 and i % n != 1 and n < i < (((m-1)*n) + 1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the top edge
        if 2 <= i <= n-1:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the bottom edge
        elif ((m-1)*n)+2 <= i <= ((m-1)*n) + (n-1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the left edge
        elif i % n == 1 and (i != 1 and i != (((m-1)*n)+1)):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the right edge
        elif i % n == 0 and (i != n and i != m*n):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the top-left corner
        elif i == 1:

            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the top-right corner
        elif i == n:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the bottom-left corner
        elif i == ((m-1)*n) + 1:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
        # i is on the bottom-right corner
        elif i == m*n:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, weightedNeutral)
            
    return g

def findExplorable(g, keys):
    """Return a list of nodes that are reachable from start using various keys"""
    reachableNodes = [1]
    edges = [e for e in g.edges(data=True) if e[2]["object"] in keys]
    for edge in edges:
        if edge[0] in reachableNodes and edge[1] not in reachableNodes:
            reachableNodes.append(edge[1])
        elif edge[1] in reachableNodes and edge[0] not in reachableNodes:
            reachableNodes.append(edge[0])
    return reachableNodes

def viableMap(dimensions, gates, weightedNeutral=0, endNode=None):

    if endNode == None:
        endNode = dimensions[0] * dimensions[1]
    
    g = createGraph(dimensions, gates, weightedNeutral, endNode)
    
    # Ensure than the final node is included in the grid
    if endNode not in g:
        return False

    # Ensure that the explorable area grows with new key discoveries
    for x in range(1, len(gates)):
        if len(findExplorable(g, gates[:x])) == \
           len(findExplorable(g, gates[:x+1])):
            return False
        
    # Find all the red edges
    primary_edges = ([e for e in g.edges(data=True) if e[2]['object']==gates[0]]
                     )
    # Determine if a red edge connects the first node to another
    for e in primary_edges:
        if e[0] == 1:
            return g
        
    return False

def generateViableMap(dimensions, gates, keys, weightedNeutral=0, endNode=None):
    # Create a viable map
    g = viableMap(dimensions, gates, weightedNeutral, endNode)
    while not g:
        g = viableMap(dimensions, gates, weightedNeutral, endNode)
    placeKeys(g, gates, keys)
    return g

def placeKeys(g, gates, keys):
    # Find random key locations within explorable zones
    for x in range(0, len(gates)-1):
        previouslyExplorable = set(findExplorable(g, gates[:x]))
        nowExplorable = set(findExplorable(g, gates[:x+1]))
        newAreas = list(nowExplorable - previouslyExplorable)
        keyLocation = random.choice(newAreas)
        keys[gates[x+1]] = keyLocation

def main():

    m = 5
    n = 5
    
    ordering = {"red":["green","blue","orange"],
                "blue":"yellow","yellow":["brown","tan"],"brown":["pink", "purple"]}
    gates = grapher.getGateOrder(ordering)

    # Create keys for each gate
    keys = {gate:1 for gate in gates}

    g = generateViableMap((m,n), gates, keys)

    # Create a color mapping to visualize key locations
    color_map = []
    for node in g:
        for gate in gates:
            if keys[gate] == node:
                color_map.append(gate)
                break
        else:
            color_map.append("grey")

    print(gates)

    #Display the graph
    pos = nx.spring_layout(g)
    #nx.draw_planar(g, with_labels=True, font_weight='bold')
    nx.draw(g, pos, node_color=color_map, with_labels=True, font_weight='bold')
    edge_labels = nx.get_edge_attributes(g,'object')
    nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
    plt.show()


if __name__ == "__main__":
    main()
        
