
import random
import graph_generation.grapher as grapher
import networkx as nx
import matplotlib.pyplot as plt

dropout = 0.4

def r():
    return random.random() > dropout

def detConnection(g, i, node, nodes, nodeStack, completedNodes, gates,
                  endNode, mapping, weightedNeutral=0):
    
    if not node in completedNodes:

        availableGates = [m[0] for m in mapping]
        gateTech = None
        
        # If the user wants more neutral connections
        if weightedNeutral != 0:
            if random.random() < weightedNeutral:
                gateTech = gates[0]
            else:
                while True:
                    gateTech = random.choice(availableGates) 
                    if gateTech != gates[0]:
                        break
        else:
             gateTech = random.choice(availableGates)

        if i == endNode or node == endNode:
            gateTech = gates[-1]

        # Check if the connection should be added 
        if r():
            
            # Create bi-directional connections between the two nodes
            # i is on the right of or below node
            tup = random.choice([m for m in mapping if m[0]==gateTech])
            if i > node:
                g.add_edge(i, node, object=tup[0])
                g.add_edge(node, i, object=tup[1])
            # i is to the left of or above node
            else:
                g.add_edge(i, node, object=tup[1])
                g.add_edge(node, i, object=tup[0])

            if node not in nodes:
                nodeStack.append(node)
                nodes.append(node)

def createGraph(dimensions, gates, mappings, weightedNeutral=0, endNode=None):

    m,n = dimensions

    g = nx.DiGraph()

    nodeStack = []
    nodes = []
    completedNodes = []
    
    nodeStack.append(1)

    while len(nodeStack) > 0:

        i = nodeStack.pop()

        # i is in the middle of the grid
        if i % n != 0 and i % n != 1 and n < i < (((m-1)*n) + 1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1], weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the top edge
        if 2 <= i <= n-1:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the bottom edge
        elif ((m-1)*n)+2 <= i <= ((m-1)*n) + (n-1):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            
        # i is on the left edge
        elif i % n == 1 and (i != 1 and i != (((m-1)*n)+1)):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the right edge
        elif i % n == 0 and (i != n and i != m*n):

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the top-left corner
        elif i == 1:

            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the top-right corner
        elif i == n:

            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            detConnection(g, i, i+n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            
        # i is on the bottom-left corner
        elif i == ((m-1)*n) + 1:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            detConnection(g, i, i+1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)
            
        # i is on the bottom-right corner
        elif i == m*n:

            detConnection(g, i, i-n, nodes, nodeStack, completedNodes, gates, endNode, mappings[1],  weightedNeutral)
            detConnection(g, i, i-1, nodes, nodeStack, completedNodes, gates, endNode, mappings[0],  weightedNeutral)

        completedNodes.append(i) 
    return g

def findExplorable(g, keys, startNode=1):
    """Return a list of nodes that are reachable from start using various keys"""
    reachableNodes = [startNode]
    prevLen = len(reachableNodes)

    # Take multiple passes to try and find edges that may have actually been reachable
    # Example is a reachable connection between 8 and 12, but 12 has the connection
    # to the greater structure
    while True:

        # Find all of the edges of a given key type
        edges = [e for e in g.edges(data=True) if e[2]["object"] in keys]

        # Iterate through the edges to find all (known) reachable nodes
        for edge in edges:
            #if not edge in reachableNodes:
                if edge[0] in reachableNodes and edge[1] not in reachableNodes:
                    reachableNodes.append(edge[1])
                elif edge[1] in reachableNodes and edge[0] not in reachableNodes:
                    if edge[2] in keys:
                        reachableNodes.append(edge[0])

        # Stop iterating if no new nodes were added
        if prevLen == len(reachableNodes):
            break
        # Save the new count of reachable nodes
        else:
            prevLen = len(reachableNodes)

    return reachableNodes

def viableMap(dimensions, gates, keys, mappings, weightedNeutral=0, endNode=None, startNode=1):

    if endNode == None:
        endNode = dimensions[0] * dimensions[1]
    
    g = createGraph(dimensions, gates, mappings, weightedNeutral, endNode)
    
    # Ensure than the final node is included in the grid
    if endNode not in g:
        return False

    # Ensure that the explorable area grows with new key discoveries
    for x in range(1, len(gates)):
        if len(findExplorable(g, gates[:x], startNode)) == \
           len(findExplorable(g, gates[:x+1], startNode)):
            return False

    # Double check that key allows new unexplored areas to be reached
    for x in range(0, len(gates)-1):
        previouslyExplorable = set(findExplorable(g, gates[:x], startNode))
        nowExplorable = set(findExplorable(g, gates[:x+1], startNode))
        newAreas = list(nowExplorable - previouslyExplorable)
        if len(newAreas) == 0:
            return False
        
    # Find all the primary edges
    primary_edges = ([e for e in g.edges(data=True) if e[2]['object']==gates[0]])
    
    # Place keys into the map
    for x in range(0, len(gates)-1):
        previouslyExplorable = set(findExplorable(g, gates[:x], startNode))
        nowExplorable = set(findExplorable(g, gates[:x+1], startNode))
        newAreas = list(nowExplorable - previouslyExplorable)

        # Check that the key is reachable from all nodes
        # That is, prevent there from being inescapable pits in the map,
        # a potential byproduct of the bidirectional structure
        keyLocation = random.choice(newAreas)

        # Create a temporary graph that only contains traversible edges
        g_temp = nx.DiGraph()
        for e in g.edges(data=True):
            if e[2]["object"] in gates[:x+1]:
                g_temp.add_edge(e[0],e[1],object=e[2]["object"])

        # Look through all of the new areas and the room
        # that contained the last key
        for node in set(newAreas + [keys[gates[x]]]):
 
            # Check that a connection of some form exists
            if not nx.has_path(g_temp, node, keyLocation):
                return False
            
        # Place the key at the given, approved node
        keys[gates[x+1]] = keyLocation

    # Determine if a primary edge connects the first node to another
    for e in primary_edges:
        if e[0] == startNode:
            return g
            
    return False

def generateViableMap(dimensions, gates, keys, mappings, weightedNeutral=0, endNode=None, startNode=1):
    # Create a viable map
    g = viableMap(dimensions, gates, keys, mappings, weightedNeutral, endNode, startNode)
    while not g:
        g = viableMap(dimensions, gates, keys, mappings, weightedNeutral, endNode, startNode)
    
    return g

def placeKeys(g, gates, keys, startNode):
    # Find random key locations within explorable zones
    for x in range(0, len(gates)-1):
        previouslyExplorable = set(findExplorable(g, gates[:x], startNode))
        nowExplorable = set(findExplorable(g, gates[:x+1], startNode))
        newAreas = list(nowExplorable - previouslyExplorable)
        keyLocation = random.choice(newAreas)
        keys[gates[x+1]] = keyLocation

def main():

    m = 4
    n = 4
    
    #ordering = {"red":["green","blue","orange"],
    #            "blue":"yellow","yellow":["brown","tan"],"brown":["pink", "purple"]}
    ordering = {"grey":"red","red":"green","green":"blue"}
    gates = grapher.getGateOrder(ordering)

    mapping = grapher.getDirectionalMapping(["grey","red",("green","orange"),"blue"])

    # Create keys for each gate
    keys = {gate:1 for gate in gates}

    g = generateViableMap((m,n), gates, keys, mapping)

    # Create a color mapping to visualize key locations
    color_map = []
    for node in g:
        for gate in gates:
            if keys[gate] == node:
                color_map.append(gate)
                break
        else:
            color_map.append("grey")

    #Display the graph
    pos = nx.spring_layout(g)
    #nx.draw_planar(g, with_labels=True, font_weight='bold')
    nx.draw(g, pos, node_color=color_map, with_labels=True, font_weight='bold')
    edge_labels = nx.get_edge_attributes(g,'object')
    nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
    plt.show()


if __name__ == "__main__":
    main()
        
