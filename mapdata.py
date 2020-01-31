class MapData():

    def __init__(self, g, keys, gates, m, n, endNode, ordering, startNode, weightedNeutral):
        self._g = g
        self._keys = keys
        self._gates = gates
        self._m = m
        self._n = n
        self._endNode = endNode
        self._ordering = ordering
        self._startNode = startNode
        self._weightedNeutral = weightedNeutral
