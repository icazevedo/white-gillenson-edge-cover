class Tree:
    def __init__(self, novo_id):
        self.id = novo_id
        self.root = None
        self.E = []
        self.O = []
        self.U = []

    def setRoot(self, root):
        root.label = 'E'
        root.tree = self.id
        self.root = root
        self.E.append(root)

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
        self.parent = None
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

class Delta:
    def __init__(self, value, edge):
        self.value = value
        self.edge = edge

    def compareAndSetDelta(self, value, edge):
        if(value < self.value or self.value is None):
            self.value = value
            self.edge = edge

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

# def delta2CalcList(E):
#     delta2CalcList = []

#     for e in E:
#         if e.v1.tree != e.v2.tree:
#             delta2CalcList.append(e.delta2And4and6())

#     return delta2CalcList

# def delta3CalcList(E):
#     delta3CalcList = []

#     for e in E:
#         if e.v1.tree != e.v2.tree:
#             delta3CalcList.append(e.alfa)

#     return delta3CalcList

# def notInCover(E, C):
#     notInCover = []
#     notInCover.extend(E)

#     for e in C:
#         notInCover.remove(e)

#     return notInCover

# def delta4CalcList(E):
#     delta4CalcList = []

#     for e in E:
#         if (e.v1.label == 'E' and e.v2.label == 'U') or e.v1.label == 'U' and e.v2.label == 'E':
#             delta4CalcList.append(e.delta2And4and6())
    
#     return delta4CalcList


# def delta5CalcList(E):
#     delta5CalcList = []

#     for e in E:
#         if (e.v1.label == 'O' and e.v2.label == 'U') or (e.v1.label == 'U' and e.v2.label == 'O'):
#             delta5CalcList.append(e.alfa)
    
#     return delta5CalcList

# def delta6CalcList(E):
#     delta6CalcList = []

#     for e in E:
#         if e.v1.tree == e.v2.tree and e.v1.label == 'E' and e.v2.label == 'E':
#             delta6CalcList.append(e.delta2And4and6())

#     return delta6CalcList

# def delta7CalcList(E):
#     delta7CalcList = []

#     for e in E:
#         if e.v1.tree == e.v2.tree and e.v1.label == 'O' and e.v2.label == 'O':
#             delta7CalcList.append(e)

#     return delta7CalcList

def pupulateForest(forest, cover_v, cover):
    for i in range(0, len(cover)):
        v_edges = cover[i]
        edge_sum = 0

        for j in range(0, len(v_edges)):
            if v_edges[j] != 0:
                edge_sum += 1

                if edge_sum > 1:
                    new_tree = forest.createNewTree()
                    new_tree.setRoot(cover_v[i])

def min_cover(adjacency_matrix):
    original_V = []
    original_E = []

    for i in range(0, len(adjacency_matrix)):
        original_V.append(Vertice(i))
    
    original_adjacency_matrix = []

    for i in range(0, len(adjacency_matrix)):
        original_adjacency_matrix[i] = []

        for j in range (i, len(adjacency_matrix[i])):
            new_edge = Edge(original_V[i], original_V[j], adjacency_matrix[i][j])

            original_adjacency_matrix.append(new_edge)
            original_E.append(new_edge)
    
    cover = original_adjacency_matrix.copy()
    cover_v = original_V.copy()

    cover_x = []

    for i in range(0, len(adjacency_matrix)):
        cover_x[i] = []

        for j in range (i, len(adjacency_matrix[i])):
            if(adjacency_matrix[i][j] == 0):
                cover_x[i][j] = 0
            else:
                cover_x[i][j] = 1

    Bp = []
    
    lambd = max(getEdgesWeight(original_E))
    wi = lambd/2

    forest = Forest()
    pupulateForest(forest, cover_v, cover)

    # for tree in forest.trees:
    #     print(tree.E)

    # for v in V:
    #     print(v)

    deltas = []

    for i in range(1, 7):
        deltas[i] = Delta(None, None)

    # CALCULAR DELTA 1
    # TODO AJEITAR DELTA 1 DEPOIS
    delta1 = 0
    delta1Valido = False

    for B in Bp:
        delta1 = 0
        delta1Valido = True

        Zps = getVerticesZp(original_V)
        
        if len(Zps) > 0:
            delta1 = min(Zps)/2
            delta1Valido = True
        else:
            delta1Valido = False

    for i in range(0, len(original_adjacency_matrix)):
        for j in range(0, len(original_adjacency_matrix[i])):
            # SE A ARESTA ESTIVER NA COBERTURA
            if cover_x[i][j] == 1:
                if cover_v[i].tree != cover_v[j].tree and cover_v[i].label == 'E' and cover_v[j].label == 'E':
                    deltas[2].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])

                if (cover_v[i].label == 'E' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'E'):
                    deltas[4].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])

                #TODO fazer verificação se i e j não estão no mesmo blossom
                if(cover_v[i].label == 'E' and cover_v[j].label == 'E') and cover_v[i].tree == cover_v[j].tree:
                    deltas[6].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])
            elif cover_x[i][j] == -1:
                if cover_v[i].tree != cover_v[j].tree and cover_v[i].label == 'O' and cover_v[j].label == 'O' and cover[i][j].alfa > 0:
                    deltas[3].compareAndSetDelta(cover[i][j].alfa, cover[i][j])

                if (cover_v[i].label == 'O' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'O') and cover[i][j].alfa > 0:
                    deltas[5].compareAndSetDelta(cover[i][j].alfa, cover[i][j])

                #TODO fazer verificação se i e j não estão no mesmo blossom
                if(cover_v[i].label == 'O' and cover_v[j].label == 'O') and cover_v[i].tree == cover_v[j].tree:
                    deltas[7].compareAndSetDelta(cover[i][j].alfa, cover[i][j])

    for i in range(1, len(deltas)):
        if (i != 4 and i != 5):
            deltas[i].compareAndSetDelta(deltas[i].value/2, deltas[i].edge)

    choosenDelta = None
    choosenDeltaIndex = None
    
    for i in range(1, len(deltas)):
        if not (deltas[i].value is None):
            if(choosenDelta is None) or (deltas[i].value < choosenDelta.value):
                choosenDelta = deltas[i]
                choosenDeltaIndex = i
    
    
    if choosenDelta is None:
        print("Found cover!")
        print(cover)
    else:
        if (choosenDeltaIndex == 2 or choosenDeltaIndex == 3):
            #Aresta verificada agora
            new_value = 0
            
            if(cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] == -1):
                new_value = 1
            elif(cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] == 1):
                new_value = -1

            cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] = new_value
            cover_x[choosenDelta.edge.v2.id][choosenDelta.edge.v1.id] = new_value

            #v1
            currentVertice = choosenDelta.edge.v1

            while(not (currentVertice.parent is None)):
                new_value = 0
                
                if(cover_x[currentVertice.id][currentVertice.parent.id] == -1):
                    new_value = 1
                elif(cover_x[currentVertice.id][currentVertice.parent.id] == 1):
                    new_value = -1
                
                cover_x[currentVertice.id][currentVertice.parent.id] = new_value
                cover_x[currentVertice.parent.id][currentVertice.id] = new_value
            
                currentVertice = currentVertice.parent

            #v2
            currentVertice = choosenDelta.edge.v2

            while(not (currentVertice.parent is None)):
                new_value = 0
                
                if(cover_x[currentVertice.id][currentVertice.parent.id] == -1):
                    new_value = 1
                elif(cover_x[currentVertice.id][currentVertice.parent.id] == 1):
                    new_value = -1
                
                cover_x[currentVertice.id][currentVertice.parent.id] = new_value
                cover_x[currentVertice.parent.id][currentVertice.id] = new_value
            
                currentVertice = currentVertice.parent
            

        if (choosenDeltaIndex == 4):
            if choosenDelta.edge.v1.label == 'E':
                choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                forest.trees[choosenDelta.edge.v1.tree].addToOdd(choosenDelta.edge.v2)
            else:
                choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                forest.trees[choosenDelta.edge.v2.tree].addToOdd(choosenDelta.edge.v1)

            # TODO fazer o caso em que o vertice não rotulado é blossom - rotular todos os vertices do blossom como odd
        elif(choosenDeltaIndex == 5):
            if choosenDelta.edge.v1.label == 'O':
                choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                forest.trees[choosenDelta.edge.v1.tree].addToEven(choosenDelta.edge.v2)
            else:
                choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                forest.trees[choosenDelta.edge.v2.tree].addToEven(choosenDelta.edge.v1)

            # TODO fazer o caso em que o vertice não rotulado é blossom - rotular todos os vertices do blossom como even
        
        for e in forest.getEven():
            e.weight = e.weight - choosenDeltaValue

        for e in forest.getOdd():
            e.weight = e.weight + choosenDeltaValue

        for v in original_V:
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