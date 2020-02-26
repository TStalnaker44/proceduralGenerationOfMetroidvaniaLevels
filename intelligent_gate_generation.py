
import networkx as nx
import random, math
import grapher
import latticeCreator

startNode = 1
m = 4
n = 5

ordering = {"neutral":"red","red":"blue","blue":"green","green":"white"}
h_mapping = ["neutral","red","blue","green","white"]
v_mapping = ["neutral","red","blue","green","white"]
gates = grapher.getGateOrder(ordering)
keys = {gate:startNode for gate in gates}
mappings = (grapher.getDirectionalMapping(h_mapping),
            grapher.getDirectionalMapping(v_mapping))
g = latticeCreator.generateViableMap((m,n), gates, keys, mappings)

def findExplorableZones(g):
    """Divide the level space into explorable zones"""

    totalNodes = g.number_of_nodes()
    potentialNodes = []
    usedNodes = [startNode]
    leafNodes = [startNode]

    previouslyExplorable = [startNode]
    nodesToAdd = math.ceil(totalNodes / len(gates))
    nodesAdded = 0
    totalNodesAdded = 0
    
    # Create distinct explorable zones for the mapping
    explorableZones = [[startNode]]

    for i in range(len(gates)):

        e_x = []
        
        while nodesAdded < nodesToAdd and totalNodes-1 != totalNodesAdded + nodesAdded:

            for node in leafNodes:
                
                for x in g.neighbors(node):
                    potentialNodes.append((node, x))
                    
            posNex = random.choice(potentialNodes)
            potentialNodes = []
            
            if not posNex[1] in usedNodes:
                usedNodes.append(posNex[1])
                leafNodes.append(posNex[1])
                e_x.append(posNex[1])
                nodesAdded += 1

            # Remove the node if its no longer a leaf node
            for y in g.neighbors(posNex[0]):
                if y not in leafNodes and y not in usedNodes: break
            else:
                leafNodes.remove(posNex[0])

        explorableZones.append(e_x)

        totalNodesAdded += nodesAdded
        nodesAdded = 0
        nodesToAdd = min(math.ceil(totalNodes / len(gates)), totalNodes-totalNodesAdded)

    return explorableZones



def getExplorableZone(node, zones):
    """Find the zone that a given node is found in"""
    for i, zone in enumerate(zones):
        if node in zone: return i

def generateConnections(g):

    newGraph = nx.DiGraph()
    explorableZones = findExplorableZones(g)

    for edge in g.edges():
        if edge[0] < edge[1]:
            z1 = getExplorableZone(edge[0], explorableZones)
            z2 = getExplorableZone(edge[1], explorableZones)
            # If the edge connects two nodes in the same explorable zone
            if z1 == z2:
                gateTech = random.choice(gates[:z1])
            # The edge connects two nodes between explorable regions
            else:
                maxZone = max(z1,z2)
                minZone = min(z1, z2)
                if abs(z1-z2)==1:
                    gateTech = gates[maxZone-1]
                else:
                    gateTech = random.choice(gates[maxZone-1:])
            
            newGraph.add_edge(edge[0],edge[1],object=edgeColor)

    return newGraph
            
##print(len(g.edges())//2)
##print(len(newGraph.edges()))
##
##for i, e in enumerate(explorableZones):
##    print("E"+str(i), e)
##
##print(sum([len(e) for e in explorableZones]))
##
grapher.plot(g)
grapher.plot(generateConnections(g))
