class Tree:
    def __init__(self, novo_id):
        self.id = novo_id
        self.E = []
        self.O = []
        self.U = []
        

    def addToEven(self, v):
        v.tree = self.id
        v.label = 'E'
        self.E.append(v)

    def addToOdd(self, v):
        v.tree = self.id
        v.label = 'O'
        self.O.append(v)

    def addToUnlabeled(self, v):
        v.tree = self.id
        v.label = 'U'
        self.U.append(v)

class Forest:
    def __init__(self):
        self.trees = []

    def createNewTree(self):
        tree = Tree(len(self.trees))
        self.addToTrees(tree)

        return tree

    def addToTrees(self, tree):
        self.trees.append(tree)

    def getEven(self):
        E = []

        for tree in self.trees:
            E.extend(tree.E)
        
        return E

    def getOdd(self):
        O = []

        for tree in self.trees:
            O.extend(tree.O)
        
        return O

    def getUnlabeled(self):
        U = []

        for tree in self.trees:
            U.extend(tree.U)
        
        return U

def getTransmitter(adjacency_matrix):
    for i in range(0, len(adjacency_matrix)):
        v = adjacency_matrix[i]
        edge_sum = 0

        for j in range(0, len(v)):
            if v[j] != 0:
                edge_sum += 1

                if edge_sum > 1:
                    return i

class Vertice:
    def __init__(self, novo_id):
        self.id = novo_id
        self.tree = -1
        self.label = 'U'
        self.weight = 0
        self.blossomVertices = []
        self.Zp = 0

    def isBlossom(self):
        return len(self.blossomVertices) > 0

    def __str__(self):
        return str(self.id) + " - " + str(self.tree) + " - " + str(self.weight)

    def __repr__(self):
        return str(self.id) + " - " + str(self.tree) + " - " + str(self.weight)

class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        self.alfa = 0
        self.x = 0
    
    def getId(self):
        return (self.v1.id, self.v2.id)
    
    def delta2And4and6(self): 
        self.v1.weight + self.v2.weight - self.weight

    def __eq__(self, value):
        return (self.v1.id == value.v1.id and self.v2.id == value.v2.id) or (self.v1.id == value.v2.id and self.v2.id == value.v1.id)

    def __str__(self):
        return "Edge from " + str(self.v1.id) + " to " + str(self.v2.id) + ". Peso " + str(self.weight) + " e alfa " + str(self.alfa)
    
    def __repr__(self):
        return "Edge from " + str(self.v1.id) + " to " + str(self.v2.id) + ". Peso " + str(self.weight) + " e alfa " + str(self.alfa)

def getEdgesWeight(E):
    weigths = []

    for e in E:
        weigths.append(e.weight)
    
    return weigths

def getVerticesZp(V):
    Zps = []

    for v in V:
        if v.isBlossom():
            Zps.append(v.Zp)
    
    return Zps

def delta2CalcList(E):
    delta2CalcList = []

    for e in E:
        if e.v1.tree != e.v2.tree:
            delta2CalcList.append(e.delta2And4and6())

    return delta2CalcList

def delta3CalcList(E):
    delta3CalcList = []

    for e in E:
        if e.v1.tree != e.v2.tree:
            delta3CalcList.append(e.alfa)

    return delta3CalcList

def notInCover(E, C):
    notInCover = []
    notInCover.extend(E)

    for e in C:
        notInCover.remove(e)

    return notInCover

def delta4CalcList(E):
    delta4CalcList = []

    for e in E:
        if (e.v1.label == 'E' and e.v2.label == 'U') or e.v1.label == 'U' and e.v2.label == 'E':
            delta4CalcList.append(e.delta2And4and6())
    
    return delta4CalcList


def delta5CalcList(E):
    delta5CalcList = []

    for e in E:
        if (e.v1.label == 'O' and e.v2.label == 'U') or (e.v1.label == 'U' and e.v2.label == 'O'):
            delta5CalcList.append(e.alfa)
    
    return delta5CalcList

def delta6CalcList(E):
    delta6CalcList = []

    for e in E:
        if e.v1.tree == e.v2.tree and e.v1.label == 'E' and e.v2.label == 'E':
            delta6CalcList.append(e.delta2And4and6())

    return delta6CalcList

def delta7CalcList(E):
    delta7CalcList = []

    for e in E:
        if e.v1.tree == e.v2.tree and e.v1.label == 'O' and e.v2.label == 'O':
            delta7CalcList.append(e)

    return delta7CalcList

def min_cover(adjacency_matrix):
    V = []
    E = []

    for i in range(0, len(adjacency_matrix)):
        V.append(Vertice(i))
    
    for i in range(0, len(adjacency_matrix)):
        for j in range (i, len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] > 0:
                E.append(Edge(V[i], V[j], adjacency_matrix[i][j]))
    
    for v in V:
        print(v)
    
    for e in E:
        print(e)
    
    Bp = []
    
    C = E
    lambd = max(getEdgesWeight(E))
    wi = lambd/2

    forest = Forest()

    transmitterIndex = getTransmitter(adjacency_matrix)

    for j in range(0, len(adjacency_matrix[transmitterIndex])):
        edge = adjacency_matrix[transmitterIndex][j]

        if edge != 0:
            tree = forest.createNewTree()
            tree.addToEven(V[j])

    # for tree in forest.trees:
    #     print(tree.E)

    # for v in V:
    #     print(v)

    # CALCULAR DELTA 1
    delta1 = 0
    delta1Valido = True

    Zps = getVerticesZp(V)
    
    if len(Zps) > 0:
        delta1 = min(Zps)/2
    else:
        delta1Valido = False

    # CALCULAR DELTA 2
    delta2 = 0
    delta2Valido = True

    delta2CalcList = delta2CalcList(C)

    if len(delta2CalcList) > 0:
        delta2 = min(delta2CalcList)/2
    else:
        delta2Valido = False

    # CALCULAR DELTA 3
    delta3 = 0
    delta3Valido = True

    delta3CalcList = delta3CalcList(notInCover(E, C))

    if len(delta3CalcList) > 0:
        delta3 = min(delta3CalcList)/2
    else:
        delta3Valido = False


    # CALCULAR DELTA 4
    delta4 = 0
    delta4Valido = True

    delta4CalcList = delta4CalcList(C)

    if len(delta4CalcList) > 0:
        delta4 = min(delta4CalcList)/2
    else:
        delta4Valido = False

    # CALCULAR DELTA 5
    delta5 = 0
    delta5Valido = True

    delta5CalcList = delta5CalcList(notInCover(E, C))

    if len(delta5CalcList) > 0:
        delta5 = min(delta5CalcList)/2
    else:
        delta5Valido = False

    # CALCULAR DELTA 6
    delta6 = 0
    delta6Valido = True

    delta6CalcList = delta6CalcList(C)

    if len(delta6CalcList) > 0:
        delta6 = min(delta6CalcList)/2
    else:
        delta6Valido = False

    # CALCULAR DELTA 7
    delta7 = 0
    delta7Valido = True

    delta7CalcList = delta7CalcList(notInCover(E, C))

    if len(delta7CalcList) > 0:
        delta7 = min(delta7CalcList)/2
    else:
        delta7Valido = False

    if not delta1Valido and not delta2Valido and not delta3Valido and not delta4Valido and not delta5Valido and not delta6Valido and not delta7Valido:
        print("Found cover!")
        print(C)
    else:
        validDeltaValues = []

        if delta1Valido:
            validDeltaValues.insert(1, delta1)
        
        if delta2Valido:
            validDeltaValues.insert(2, delta2)

        if delta3Valido:
            validDeltaValues.insert(3, delta3)

        if delta4Valido:
            validDeltaValues.insert(4, delta4)

        if delta5Valido:
            validDeltaValues.insert(5, delta5)

        if delta6Valido:
            validDeltaValues.insert(6, delta6)

        if delta7Valido:
            validDeltaValues.insert(7, delta7)

        choosenDeltaValue = min(validDeltaValues)
        choosenDelta = -1

        for validDeltaIndex in range(1, 8):
            if validDeltaValues[validDeltaIndex] == choosenDeltaValue:
                choosenDelta = validDeltaIndex
                break

        for e in forest.getEven():
            e.weight = e.weight - choosenDeltaValue

        for e in forest.getOdd():
            e.weight = e.weight + choosenDeltaValue

        for v in V:
            if v.isBlossom():
                if v.label == 'E':
                    v.Zp = v.Zp - (2 * choosenDeltaValue)
                elif v.label == 'O':
                    v.Zp = v.Zp + (2 * choosenDeltaValue)

        for e in notInCover(C):
            isInSameBlossom = False

            for b in Bp:
                if b.blossomVertices.index(e.v1) != -1 and b.blossomVertices.index(e.v2) != -1:
                    isInSameBlossom = True
                    break
            
            if isInSameBlossom:
                pass
            
            if e.v1.label == 'O' and e.v2.label == 'O':
                e.alfa = e.alfa - (2 * choosenDeltaValue)
            elif e.v1.label == 'E' and e.v2.label == 'E':
                e.alfa = e.alfa + (2 * choosenDeltaValue)
            elif  (e.v1.label == 'O' and e.v2.label == 'U') or (e.v1.label == 'U' and e.v2.label == 'O'):
                e.alfa = e.alfa - (choosenDeltaValue)
            elif  (e.v1.label == 'E' and e.v2.label == 'U') or (e.v1.label == 'U' and e.v2.label == 'E'):
                e.alfa = e.alfa + (choosenDeltaValue)

            lambd = lambd - (2 * choosenDeltaValue)

                


ma = [
    [0, 20, 0, 0, 10, 0],
    [1, 0, 5, 0, 2, 0],
    [0, 1, 0, 5, 0, 0],
    [0, 0, 1, 0, 4, 2],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0]
]

min_cover(ma)