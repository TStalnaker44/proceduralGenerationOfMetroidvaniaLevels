
class MapData():
    """Class that represents a template for making maps.  That
    is to say that an instance of this class can be used as a
    seed to generate many distinct, yet similar maps"""

    def __init__(self, g, keys, gates, m, n, endNode, ordering,
                 startNode, weightedNeutral):
        self._g = g
        self._keys = keys
        self._gates = gates
        self._m = m
        self._n = n
        self._endNode = endNode
        self._ordering = ordering
        self._startNode = startNode
        self._weightedNeutral = weightedNeutral

class GeneratedMap():
    """Class that represents a fully generated map.  That is that
    instances of this class represent a unique representation of a
    map in the platforming view of the game."""

    def __init__(self, templateData, finish, walls, platforms, physicalKeys,
                 playerStart):
        self._templateData = templateData
        self._finish = finish
        self._walls = walls
        self._platforms = platforms
        self._physicalKeys = physicalKeys
        self._playerStart = playerStart
        
