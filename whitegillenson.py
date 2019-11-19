class Tree:
    def __init__(self, novo_id):
        self.id = novo_id
        self.root = None
        self.vertices = []

    def setRoot(self, root):
        root.label = 'E'
        root.tree = self.id
        self.root = root
        self.vertices.append(root)

    def addToEven(self, v):
        v.tree = self.id
        v.label = 'E'
        self.vertices.append(v)

    def addToOdd(self, v):
        v.tree = self.id
        v.label = 'O'
        self.vertices.append(v)

    def addToUnlabeled(self, v):
        v.tree = self.id
        v.label = 'U'
        self.vertices.append(v)

class Forest:
    def __init__(self):
        self.trees = []

    def createNewTree(self):
        tree = Tree(len(self.trees))
        self.addToTrees(tree)

        return tree

    def addToTrees(self, tree):
        self.trees.append(tree)

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
        self.children = []
        self.blossomEdges = []
        self.blossomVerticesId = []
        self.Zp = 0

    def isBlossom(self):
        return len(self.blossomEdges) > 0

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
        self.originalEdge = None
    
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
        self.blossom = None

    def compareAndSetDelta(self, value, edge):
        if(value < self.value or self.value is None):
            self.value = value
            self.edge = edge

    def compareAndSetDelta1(self, value, blossom):
        if(value < self.value or self.value is None):
            self.value = value
            self.blossom = blossom

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
            if adjacency_matrix[i][j] != 0:
                new_edge = Edge(original_V[i], original_V[j], adjacency_matrix[i][j])

                original_adjacency_matrix.append(new_edge)
                original_E.append(new_edge)
            else:
                original_adjacency_matrix.append(None)
    
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

    #Calculando Delta 1
    for B in Bp:
        deltas[1].compareAndSetDelta1(B.Zp, B)

    for i in range(0, len(original_adjacency_matrix)):
        for j in range(0, len(original_adjacency_matrix[i])):
            # SE A ARESTA ESTIVER NA COBERTURA
            if cover_x[i][j] == 1:
                if cover_v[i].tree != cover_v[j].tree and cover_v[i].label == 'E' and cover_v[j].label == 'E':
                    deltas[2].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])

                if (cover_v[i].label == 'E' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'E'):
                    deltas[4].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])

                if(cover_v[i].label == 'E' and cover_v[j].label == 'E') and cover_v[i].tree == cover_v[j].tree:
                    notInSameBlossom = True

                    for B in Bp:
                        if B.blossomVerticesId.count(i) > 0 and B.blossomVerticesId.count(j) > 0:
                            notInSameBlossom = False
                            break
                    
                    if notInSameBlossom:
                        deltas[6].compareAndSetDelta(cover[i][j].delta2And4and6(), cover[i][j])
            elif cover_x[i][j] == -1:
                if cover_v[i].tree != cover_v[j].tree and cover_v[i].label == 'O' and cover_v[j].label == 'O' and cover[i][j].alfa > 0:
                    deltas[3].compareAndSetDelta(cover[i][j].alfa, cover[i][j])

                if (cover_v[i].label == 'O' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'O') and cover[i][j].alfa > 0:
                    deltas[5].compareAndSetDelta(cover[i][j].alfa, cover[i][j])

                if(cover_v[i].label == 'O' and cover_v[j].label == 'O') and cover_v[i].tree == cover_v[j].tree:
                    notInSameBlossom = True

                    for B in Bp:
                        if B.blossomVerticesId.count(i) > 0 and B.blossomVerticesId.count(j) > 0:
                            notInSameBlossom = False
                            break
                    
                    if notInSameBlossom:
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
        print(cover_x)
    else:
        if (choosenDeltaIndex == 1):
            def isTransmitter(i):
                count = 0
                for j in range(0, len(cover[i])):
                    if ((not (cover[i][j] is None)) and cover_x[i][j] == 1):
                        count += 1
                    
                        if count > 1:
                            return True

                return False
                

            def reconsctructTree(tree, v, lastCoverX):
                for j in range(0, cover[v]):
                    #EVEN TO ODD
                    if(cover_x[i][j] == 1 and lastCoverX == -1):
                        if(isTransmitter(j) or not cover_v[j].tree == -1):
                            return
                        else:
                            tree.addToOdd(cover_v[j])
                            reconsctructTree(tree, j, 1)
                    #ODD TO EVEN
                    elif(cover_x[i][j] == -1 and lastCoverX == 1):
                        if(cover_v[j].tree == -1):
                            tree.addToEven(cover_v[j])
                            reconsctructTree(tree, j, -1)


            blossom_tree = forest.trees[choosenDelta.blossom.tree]
            for vertice in blossom_tree.vertices:
                vertice.tree = -1
                vertice.label = 'U'
            
            blossom_tree.vertices = []

            choosenDelta.blossom.tree = -1
            choosenDelta.blossom.label = 'U'
            
            reconsctructTree(blossom_tree, blossom_tree.root.id, -1)
            # new_alternating_tree = Tree(choosenDelta.blossom.tree)
            # new_alternating_tree.setRoot(blossom_tree.root)

            # choosenDelta.blossom.tree = -1
            # choosenDelta.blossom.parent = None
            # choosenDelta.blossom.blossomEdges = []
            # choosenDelta.blossom.blossomVerticesId = []
            # choosenDelta.blossom.label = 'U'

            # def crescerArvoreAlternada():
            #     blossom_tree = forest.trees[choosenDelta.blossom.tree]
            #     choosenDelta.blossom.tree = -1
            #     choosenDelta.blossom.parent = None
            #     choosenDelta.blossom.blossomEdges = []
            #     choosenDelta.blossom.blossomVerticesId = []
            #     choosenDelta.blossom.label = 'U'

            # edges = len(choosenDelta.blossom.blossomEdges)

            # for i in blossom_tree.vertices:
            #     if(not (cover[i][choosenDelta.blossom.id] is None)):
            #         originalEdgeTuple = cover[i][choosenDelta.blossom.id]
            #         originalEdge = cover[originalEdgeTuple[0]][originalEdgeTuple[1]]

            #         novo_vertice = cover_v[originalEdgeTuple[1]]
            #         continuar = True
            #         while continuar:
            #             if(cover_v[originalEdgeTuple[0]].label == 'O'):
            #                 blossom_tree.addToEven(novo_vertice)
            #             elif(cover_v[originalEdgeTuple[0]].label == 'E'):
            #                 blossom_tree.addToOdd(novo_vertice)

            #         previousEdgeInCover = cover_x[originalEdgeTuple[0]][originalEdgeTuple[1]] == 1
            #         previrousEdgeLabel = cover_v[originalEdgeTuple[0]].label

            # for edge in choosenDelta.blossom.blossomEdges:
                

                # if (choosenDelta.blossom.blossomVerticesId.count() > 1):

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
            

        elif (choosenDeltaIndex == 4):
            if choosenDelta.edge.v1.label == 'E':
                choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                choosenDelta.edge.v1.children.append(choosenDelta.edge.v2)
                forest.trees[choosenDelta.edge.v1.tree].addToOdd(choosenDelta.edge.v2)
            else:
                choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                choosenDelta.edge.v2.children.append(choosenDelta.edge.v1)
                forest.trees[choosenDelta.edge.v2.tree].addToOdd(choosenDelta.edge.v1)

            # TODO fazer o caso em que o vertice não rotulado é blossom - rotular todos os vertices do blossom como odd
        elif(choosenDeltaIndex == 5):
            if choosenDelta.edge.v1.label == 'O':
                choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                choosenDelta.edge.v1.children.append(choosenDelta.edge.v2)
                forest.trees[choosenDelta.edge.v1.tree].addToEven(choosenDelta.edge.v2)
            else:
                choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                choosenDelta.edge.v2.children.append(choosenDelta.edge.v1)
                forest.trees[choosenDelta.edge.v2.tree].addToEven(choosenDelta.edge.v1)

            # TODO fazer o caso em que o vertice não rotulado é blossom - rotular todos os vertices do blossom como even
        elif(choosenDeltaIndex == 6 or choosenDeltaIndex == 7):
            edge_tree = forest.trees[choosenDelta.edge.v1.tree]
            root_of_tree = edge_tree.root

            root_degree = 0

            for edge_x in cover_x[root_of_tree.id]:
                if edge_x == 1:
                    root_degree += 1
            
            isTypeOneBlossomCheck1 = False
            isTypeOneBlossomCheck2 = False

            if(cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] == 1):
                currentVertice = choosenDelta.edge.v1
                while(not (currentVertice.parent is None)):
                    if(currentVertice.parent.parent is None):
                        isTypeOneBlossomCheck1 = cover_x[currentVertice.parent.id][currentVertice.parent.parent.id] == 1
                        break

                    else:
                        currentVertice = currentVertice.parent


                if (isTypeOneBlossomCheck1):
                    currentVertice = choosenDelta.edge.v2
                    while(not (currentVertice.parent is None)):
                        if(currentVertice.parent.parent is None):
                            isTypeOneBlossomCheck2 = cover_x[currentVertice.parent.id][currentVertice.parent.parent.id] == 1
                            break

                        else:
                            currentVertice = currentVertice.parent

            if root_degree > 2 and isTypeOneBlossomCheck1 and isTypeOneBlossomCheck2:
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
            else:
                #Instanciação do pseudo-vertice que representa o blossom
                blossom_vertice = Vertice(len(cover[i]))

                blossom_vertices = edge_tree.vertices

                v1_path = []
                v2_path = []

                currentV1 = choosenDelta.v1
                currentV2 = choosenDelta.v2
                
                while(not (currentV1.parent is None)):
                    while(not (currentV2,parent is None)):
                        if currentV1.parent.id == currentV2.parent.id:
                            currentV2 = currentV2.parent

                blossom_vertices_id = []

                #Muda o rótulo de todos os vértices que compõem o blossom
                for bv in blossom_vertices:
                    bv.label = 'O'
                    blossom_vertices_id.append(bv.id)

                blossom_vertice.blossomVerticesId = blossom_vertices_id

                #Cria novo vertice na cobertura (matriz de adjacencia)
                cover.append([])
                cover_x.append([])
                
                for i in range(0, len(cover) - 1):
                    #Variavel que indica se uma relação do vertice i foi encontrada com algum vértice j que está no blossom
                    found = False

                    #Se o vertice não está no blossom
                    if blossom_vertices_id.count(i) == 0:
                        for j in range(0, len(cover[i])):
                            #Considera onde tem aresta e se o j está no blossom - ou seja, é uma aresta que se conecta ao pseudo-vertice
                            if (not (cover[i][j] is None)) and blossom_vertices_id.count(j) > 0:
                                new_blossom_relation = Edge(blossom_vertice, cover_v[i], cover[i][j].weight)
                                new_blossom_relation.originalEdge = (i, j)

                                #Define a relação do lado do pseudo-vertice
                                cover[len(cover) - 1].append(new_blossom_relation)
                                cover_x[len(cover) - 1].append(cover_x[i][j])

                                #Define a relação do lado do vertice já existente
                                cover[i].append(new_blossom_relation)
                                cover_x[i].append(cover_x[i][j])

                                #Encerra a execução para o vértice
                                found = True
                                break
                    else:
                        #Se o vértice i estiver no blossom
                        for j in range(0, len(cover[i])):

                            #Verifica se o vértice j está no blossom, se sim, adiciona a aresta entre eles ao pseudo-vertice
                            if (not (cover[i][j] is None)) and blossom_vertices_id.count(j) > 0:
                                blossom_vertice.blossomEdges.append(cover[i][j])
                    
                    #Se não foi encontrada uma aresta que conecta o vertice i ao blossom, é criada uma relação nula que representa a ausencia de relação
                    if not found:
                        #Criando relação nula do lado do pseudo-vertice
                        cover[len(cover) - 1].append(None)
                        cover_x[len(cover) - 1].append(0)

                        #Criando relação nula do lado do vértice existente
                        cover[i].append(None)
                        cover_x[i].append(0)

                cover[len(cover) - 1].append(None)
                cover_x[len(cover) - 1].append(0)

                Bp.append(blossom_vertice)


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
                if b.blossomEdges.index(e.v1) != -1 and b.blossomEdges.index(e.v2) != -1:
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