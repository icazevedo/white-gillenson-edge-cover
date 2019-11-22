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

    def removeTree(self, tree_id):
        for v in self.trees[tree_id].vertices:
            v.label = 'U'
            v.tree = -1
            v.parent = None
            v.children = []

        self.trees.pop(tree_id)

        for i in range(0, len(self.trees)):
            self.trees[i].id = i

            for v in self.trees[i].vertices:
                v.tree = i

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
        self.distinguishedVertex = []
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
        return self.v1.weight + self.v2.weight - self.weight

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
        if(self.value is None or (value < self.value and value >= 0)):
            self.value = value
            self.edge = edge

    def compareAndSetDelta1(self, value, blossom):
        if(self.value is None or  (value < self.value and value >= 0)):
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

def populateForest(forest, cover_v, cover, cover_x):
    for i in range(0, len(cover)):
        v_edges = cover[i]
        edge_sum = 0

        if(cover_v[i].label == 'U' and cover_v[i].tree == -1):
            for j in range(0, len(v_edges)):
                if (not (v_edges[j] is None)) and cover_x[i][j] == 1:
                    edge_sum += 1

                    if edge_sum > 1:
                        new_tree = forest.createNewTree()
                        new_tree.setRoot(cover_v[i])
                        break

def min_cover(adjacency_matrix):
    original_V = []
    original_E = []

    for i in range(0, len(adjacency_matrix)):
        original_V.append(Vertice(i))
    
    original_adjacency_matrix = []

    for i in range(0, len(adjacency_matrix)):
        original_adjacency_matrix.append([])

        for j in range (0, len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] != 0:
                new_edge = Edge(original_V[i], original_V[j], adjacency_matrix[i][j])

                original_adjacency_matrix[i].append(new_edge)
                original_E.append(new_edge)
            else:
                original_adjacency_matrix[i].append(None)
    
    cover = original_adjacency_matrix.copy()
    cover_v = original_V.copy()

    cover_x = []

    for i in range(0, len(adjacency_matrix)):
        cover_x.append([])

        for j in range (0, len(adjacency_matrix[i])):
            if(adjacency_matrix[i][j] == 0):
                cover_x[i].append(0)
            else:
                cover_x[i].append(1)

    Bp = []
    
    lambd = max(getEdgesWeight(original_E))
    wi = lambd/2

    for i in range(0, len(cover)):
        cover_v[i].weight = lambd/2

        for j in range(0, len(cover[i])):
            if(not (cover[i][j] is None)):
                cover[i][j].alfa = 0

    #FAZER PASSO 2
    forest = Forest()

    continuarPasso2 = True

    while(continuarPasso2):
        continuarPasso2 = False

        populateForest(forest, cover_v, cover, cover_x)

        continuarPasso3 = True
        while(continuarPasso3):
            continuarPasso3 = False

            deltas = [None]

            for i in range(0, 7):
                deltas.append(Delta(None, None))

            #Calculando Delta 1
            for B in Bp:
                if B.label == 'E':
                    deltas[1].compareAndSetDelta1(B.Zp, B)

            for i in range(0, len(cover) - len(Bp)):
                ii = i
                for j in range(0, len(cover[i]) - len(Bp)):
                    jj = j
                    
                    # SE A ARESTA ESTIVER NA COBERTURA
                    if (not(cover[ii][jj] is None)) and cover_x[ii][jj] == 1:
                        if cover_v[ii].tree != cover_v[jj].tree and cover_v[ii].label == 'E' and cover_v[jj].label == 'E':
                            deltas[2].compareAndSetDelta(cover[ii][jj].delta2And4and6(), cover[ii][jj])

                        if (cover_v[ii].label == 'E' and cover_v[jj].label == 'U') or (cover_v[ii].label == 'U' and cover_v[jj].label == 'E'):
                            deltas[4].compareAndSetDelta(cover[ii][jj].delta2And4and6(), cover[ii][jj])

                        if(cover_v[ii].label == 'E' and cover_v[jj].label == 'E') and cover_v[ii].tree == cover_v[jj].tree:
                            notInSameBlossom = True

                            for B in Bp:
                                if B.blossomVerticesId.count(ii) > 0 and B.blossomVerticesId.count(jj) > 0:
                                    notInSameBlossom = False
                                    break
                            
                            if notInSameBlossom:
                                deltas[6].compareAndSetDelta(cover[ii][jj].delta2And4and6(), cover[ii][jj])
                    elif (not(cover[ii][jj] is None)) and cover_x[ii][jj] == -1:      
                        if cover_v[ii].tree != cover_v[jj].tree and cover_v[ii].label == 'O' and cover_v[jj].label == 'O':
                            deltas[3].compareAndSetDelta(cover[ii][jj].alfa, cover[ii][jj])

                        if (cover_v[ii].label == 'O' and cover_v[jj].label == 'U') or (cover_v[ii].label == 'U' and cover_v[jj].label == 'O'):
                            deltas[5].compareAndSetDelta(cover[ii][jj].alfa, cover[ii][jj])

                        if(cover_v[ii].label == 'O' and cover_v[jj].label == 'O') and cover_v[ii].tree == cover_v[jj].tree:
                            notInSameBlossom = True

                            for B in Bp:
                                if B.blossomVerticesId.count(ii) > 0 and B.blossomVerticesId.count(jj) > 0:
                                    notInSameBlossom = False
                                    break
                            
                            if notInSameBlossom:
                                deltas[7].compareAndSetDelta(cover[ii][jj].alfa, cover[ii][jj])

            for i in range(1, len(deltas)):
                if (i != 4 and i != 5) and (not (deltas[i].value is None)):
                    deltas[i].compareAndSetDelta(deltas[i].value/2, deltas[i].edge)

            choosenDelta = None
            choosenDeltaIndex = None
            
            for i in range(1, len(deltas)):
                if not (deltas[i].value is None):
                    if(choosenDelta is None) or (deltas[i].value < choosenDelta.value):
                        choosenDelta = deltas[i]
                        choosenDeltaIndex = i
            
            
            print(lambd)
            if choosenDelta is None:
                print("Found cover!")
                print(cover)
                print(cover_x)
            else:
                #AJUSTANDO VALORES
                for v in cover_v:
                    if(v.label == 'E'):
                        v.weight = v.weight - choosenDelta.value

                        if(v.isBlossom()):
                            v.Zp = v.Zp - (2 * choosenDelta.value)
                    elif(v.label == 'O'):
                        v.weight = v.weight + choosenDelta.value

                        if(v.isBlossom()):
                            v.Zp = v.Zp + (2 * choosenDelta.value)

                for i in range(0, len(cover) - len(Bp)):
                    for j in range(0, len(cover[i]) - len(Bp)):
                        # SE A ARESTA NAO ESTIVER NA COBERTURA
                        if (not (cover[i][j] is None)) and (cover_x[i][j] == -1):              
                            notInSameBlossom = True

                            for B in Bp:
                                if B.blossomVerticesId.count(i) > 0 and B.blossomVerticesId.count(j) > 0:
                                    notInSameBlossom = False
                                    break
                            
                            if notInSameBlossom:
                                if(cover_v[i].label == 'O' and cover_v[j].label == 'O'):
                                    cover[i][j].alfa = cover[i][j].alfa - (2 * choosenDelta.value)
                                elif((cover_v[i].label == 'O' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'O')):
                                    cover[i][j].alfa = cover[i][j].alfa - (choosenDelta.value)
                                elif((cover_v[i].label == 'E' and cover_v[j].label == 'U') or (cover_v[i].label == 'U' and cover_v[j].label == 'E')):
                                    cover[i][j].alfa = cover[i][j].alfa + (choosenDelta.value)
                                elif(cover_v[i].label == 'E' and cover_v[j].label == 'E'):
                                    cover[i][j].alfa = cover[i][j].alfa + (2 * choosenDelta.value)

                lambd = lambd - (2 * choosenDelta.value)

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
                        for j in range(0, len(cover[v])):
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
                    continuarPasso3 = True
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

                    v1_original_tree = choosenDelta.edge.v1.tree

                    for v in forest.trees[choosenDelta.edge.v1.tree].vertices:
                        v.label = 'U'
                        v.tree = -1

                        for child in v.children:
                            new_value = 0
                            
                            if(cover_x[v.id][child.id] == -1):
                                new_value = 1
                            elif(cover_x[v.id][child.id] == 1):
                                new_value = -1
                            
                            cover_x[v.id][child.id] = new_value
                            cover_x[child.id][v.id] = new_value

                        v.parent = None
                        v.children = []

                    forest.removeTree(v1_original_tree)

                    v2_original_tree = choosenDelta.edge.v2.tree

                    for v in forest.trees[choosenDelta.edge.v2.tree].vertices:
                        v.label = 'U'
                        v.tree = -1
                        
                        if (not (v.parent is None)):
                            new_value = 0
                            
                            if(cover_x[v.id][v.parent.id] == -1):
                                new_value = 1
                            elif(cover_x[v.id][v.parent.id] == 1):
                                new_value = -1
                            
                            cover_x[v.id][v.parent.id] = new_value
                            cover_x[v.parent.id][v.id] = new_value

                        v.parent = None

                    forest.removeTree(v2_original_tree)

                    continuarPasso2 = True
                elif (choosenDeltaIndex == 4):
                    #v1 está na arvore
                    if choosenDelta.edge.v1.label == 'E':
                        choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                        choosenDelta.edge.v1.children.append(choosenDelta.edge.v2)
                        forest.trees[choosenDelta.edge.v1.tree].addToOdd(choosenDelta.edge.v2)

                        if(choosenDelta.edge.v2.isBlossom()):
                            for i in choosenDelta.edge.v2.blossomVerticesId:
                                cover_v[i].label = 'O'

                    #v2 é que está na árvore
                    else:
                        choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                        choosenDelta.edge.v2.children.append(choosenDelta.edge.v1)
                        forest.trees[choosenDelta.edge.v2.tree].addToOdd(choosenDelta.edge.v1)

                        if(choosenDelta.edge.v1.isBlossom()):
                            for i in choosenDelta.edge.v1.blossomVerticesId:
                                cover_v[i].label = 'O'
                    

                    cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] = 1
                    cover_x[choosenDelta.edge.v2.id][choosenDelta.edge.v1.id] = 1

                    continuarPasso3 = True
                elif(choosenDeltaIndex == 5):
                    #v1 está na arvore
                    if choosenDelta.edge.v1.label == 'O':
                        choosenDelta.edge.v2.parent = choosenDelta.edge.v1
                        choosenDelta.edge.v1.children.append(choosenDelta.edge.v2)
                        forest.trees[choosenDelta.edge.v1.tree].addToEven(choosenDelta.edge.v2)

                        if(choosenDelta.edge.v2.isBlossom()):
                            for i in choosenDelta.edge.v2.blossomVerticesId:
                                cover_v[i].label = 'E'
                    #v2 está na arvore
                    else:
                        choosenDelta.edge.v1.parent = choosenDelta.edge.v2
                        choosenDelta.edge.v2.children.append(choosenDelta.edge.v1)
                        forest.trees[choosenDelta.edge.v2.tree].addToEven(choosenDelta.edge.v1)

                        if(choosenDelta.edge.v1.isBlossom()):
                            for i in choosenDelta.edge.v1.blossomVerticesId:
                                cover_v[i].label = 'E'

                    cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] = -1
                    cover_x[choosenDelta.edge.v2.id][choosenDelta.edge.v1.id] = -1
                    
                    continuarPasso3 = True
                elif(choosenDeltaIndex == 6 or choosenDeltaIndex == 7):
                    edge_tree = forest.trees[choosenDelta.edge.v1.tree]
                    root_of_tree = edge_tree.root

                    root_degree = 0

                    for edge_x in cover_x[root_of_tree.id]:
                        if edge_x == 1:
                            root_degree += 1
                    
                    isTypeOneBlossomCheck = False

                    v1_path = []
                    v2_path = []

                    currentV1 = choosenDelta.edge.v1
                    currentV2 = choosenDelta.edge.v2
                    
                    foundDistinguishedVertex = False
                    distinguishedVertex = None

                    #encontra circuito do blossom
                    while(not (currentV1 is None)):
                        if foundDistinguishedVertex:
                            break

                        if(not foundDistinguishedVertex):
                            v2_path = []
                            currentV2 = choosenDelta.edge.v2
                            while(not (currentV2 is None)):
                                if currentV1.id == currentV2.id:
                                    foundDistinguishedVertex = True
                                    distinguishedVertex = currentV1
                                    break

                                v2_path.append(currentV2.id)
                                currentV2 = currentV2.parent

                            if not foundDistinguishedVertex:
                                v1_path.append(currentV1.id)

                            currentV1 = currentV1.parent
                    
                    isTypeOneBlossomCheck = (len(v1_path) == 0 or cover_x[distinguishedVertex.id][v1_path[-1]] == 1) and (len(v2_path) == 0 or cover_x[distinguishedVertex.id][v2_path[-1]] == 1)

                    if root_degree > 2 and isTypeOneBlossomCheck:
                        #Aresta verificada agora
                        new_value = 0
                        
                        if(cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] == -1):
                            new_value = 1
                        elif(cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] == 1):
                            new_value = -1

                        cover_x[choosenDelta.edge.v1.id][choosenDelta.edge.v2.id] = new_value
                        cover_x[choosenDelta.edge.v2.id][choosenDelta.edge.v1.id] = new_value

                        original_tree_id = choosenDelta.edge.v1.tree

                        for v in forest.trees[choosenDelta.edge.v1.tree].vertices:
                            v.label = 'U'
                            v.tree = -1

                            if (not (v.parent is None)):
                                new_value = 0
                                
                                if(cover_x[v.id][v.parent.id] == -1):
                                    new_value = 1
                                elif(cover_x[v.id][v.parent.id] == 1):
                                    new_value = -1
                                
                                cover_x[v.id][v.parent.id] = new_value
                                cover_x[v.parent.id][v.id] = new_value
                            
                            v.parent = None
                            v.children = []

                        forest.removeTree(original_tree_id)

                        continuarPasso2 = True
                    else:
                        #Instanciação do pseudo-vertice que representa o blossom
                        blossom_vertice = Vertice(len(cover[i]))

                        choosenDelta.edge.v1.children.append(choosenDelta.edge.v2)

                        v1_path = []
                        v2_path = []

                        currentV1 = choosenDelta.edge.v1
                        currentV2 = choosenDelta.edge.v2
                        
                        foundDistinguishedVertex = False
                        distinguishedVertex = None

                        #encontra circuito do blossom
                        while(not (currentV1 is None)):
                            if foundDistinguishedVertex:
                                break

                            if(not foundDistinguishedVertex):
                                v2_path = []
                                currentV2 = choosenDelta.edge.v2
                                while(not (currentV2 is None)):
                                    if currentV1.id == currentV2.id:
                                        foundDistinguishedVertex = True
                                        distinguishedVertex = currentV1
                                        break

                                    v2_path.append(currentV2.id)
                                    currentV2 = currentV2.parent

                                if not foundDistinguishedVertex:
                                    v1_path.append(currentV1.id)

                                currentV1 = currentV1.parent

                        blossom_vertices_id = []
                        blossom_vertices_id.append(distinguishedVertex.id)
                        blossom_vertices_id.extend(v1_path)
                        blossom_vertices_id.extend(v2_path)

                        #Muda o rótulo de todos os vértices que compõem o blossom
                        for bv in blossom_vertices_id:
                            cover_v[bv].label = 'O'

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
                                for j in range(i, len(cover[i])):

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

                        forest.trees[choosenDelta.edge.v1.tree].addToOdd(blossom_vertice)
                        cover_v.append(blossom_vertice)

                        Bp.append(blossom_vertice)
                        continuarPasso3 = True

# ma = [
#     [0, 9, 0, 0, 0, 0, 0, 0, 0, 0],
#     [9, 0, 22, 0, 0, 0, 0, 0, 0, 0],
#     [0, 22, 0, 34, 0, 0, 0, 0, 0, 0],
#     [0, 0, 34, 0, 27, 25, 0, 0, 0, 0],
#     [0, 0, 0, 27, 0, 26, 0, 0, 0, 0],
#     [0, 0, 0, 25, 26, 0, 28, 0, 0, 0],
#     [0, 0, 0, 0, 0, 28, 0, 21, 0, 24],
#     [0, 0, 0, 0, 0, 0, 21, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 2],
#     [0, 0, 0, 0, 0, 0, 24, 0, 2, 0]
# ]


ma = [[0, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 0, 0, 0], [92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 130, 0, 0, 0, 0, 0, 0, 0, 227, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 127, 0, 0, 0], [0, 0, 0, 0, 0, 225, 232, 0, 0, 233, 0, 0, 0, 188, 0, 0, 0, 246, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 148, 0, 0, 189, 163, 0, 0, 201, 0, 0, 0, 0, 211, 0, 0, 117, 0, 105, 0, 0, 0, 0, 0, 0, 193, 166, 0, 0, 0, 0, 0, 237, 69, 153, 0, 0, 0, 237, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 236, 0, 0, 0, 0, 0, 0, 0, 125, 0, 0, 0, 0, 0, 0, 217, 0, 0, 0, 0, 0, 0, 0, 229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 147, 0, 0, 0, 0, 0, 0, 89, 0, 0, 0, 0, 237, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 178, 127, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 135, 238, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 166, 0, 0, 0, 0, 0, 0, 0, 213, 0, 0, 220, 177, 0, 0, 0, 0, 0, 0, 190, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 225, 0, 0, 0, 215, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 181, 0, 0, 237, 0, 0, 0, 73, 0, 0, 0, 0, 0, 0, 0, 139, 0, 0, 0, 0, 0, 0, 0, 0, 151, 79, 0, 0, 0, 0, 0, 0, 0, 154, 0, 0, 0, 0, 0, 0], [0, 0, 232, 0, 0, 215, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 212, 0, 0, 0, 0, 0, 0, 108, 0, 0, 0, 84, 0, 0, 64, 135, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 134, 0, 0, 0, 0, 0, 0, 0, 0, 65, 150, 0, 0, 0, 0, 0, 0, 219, 0, 0, 0, 0, 145, 200, 0], [0, 0, 0, 0, 0, 0, 0, 0, 163, 0, 0, 0, 76, 138, 84, 0, 0, 0, 144, 200, 0, 0, 0, 0, 0, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 136, 0, 0, 0, 184], [0, 0, 0, 0, 0, 0, 0, 163, 0, 0, 0, 0, 132, 170, 188, 0, 0, 0, 0, 0, 130, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 0, 224, 0, 0, 169, 117, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 228, 0, 0, 0, 0, 0, 0, 0, 228, 0, 0, 0, 0, 0, 0, 0, 67], [0, 0, 233, 236, 0, 0, 0, 0, 0, 0, 174, 146, 0, 0, 0, 0, 52, 192, 0, 0, 0, 133, 0, 0, 0, 0, 0, 0, 0, 0, 218, 0, 221, 163, 0, 0, 0, 0, 0, 0, 62, 238, 137, 0, 0, 167, 0, 0, 0, 198, 0, 0, 0, 0, 0, 0, 170, 0, 176, 134, 175, 0, 0, 0, 0, 248, 0, 0], [0, 0, 0, 0, 135, 0, 0, 0, 0, 174, 0, 104, 0, 0, 0, 0, 145, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 71, 0, 0, 223, 0, 0, 0, 0, 0, 0, 208, 122, 125, 0, 0, 0, 0, 0, 0, 185, 0, 0, 0, 0, 0, 0, 168, 0, 234, 242, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 238, 0, 0, 0, 0, 146, 104, 0, 0, 0, 0, 0, 95, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 0, 0, 122, 0, 0, 0, 0, 0, 0, 146, 95, 186, 0, 0, 0, 0, 0, 0, 0, 0, 186, 0, 0, 0, 0, 64, 0, 0, 152, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 76, 132, 0, 0, 0, 0, 190, 55, 0, 0, 0, 186, 212, 0, 0, 0, 0, 0, 74, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 222, 163, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 207, 0, 0, 0, 125], [0, 0, 188, 0, 0, 0, 0, 138, 170, 0, 0, 0, 190, 0, 220, 0, 0, 0, 0, 0, 244, 196, 0, 0, 0, 198, 0, 0, 0, 0, 0, 0, 0, 214, 0, 0, 0, 0, 0, 0, 215, 0, 0, 0, 0, 126, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 174, 221, 223, 0, 183, 0, 0, 0, 229], [0, 0, 0, 0, 0, 0, 0, 84, 188, 0, 0, 0, 55, 220, 0, 0, 0, 0, 141, 157, 0, 0, 0, 0, 0, 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 208, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 187, 0, 0, 0, 177], [92, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 143, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 52, 145, 95, 0, 0, 0, 0, 0, 243, 0, 0, 0, 170, 0, 0, 0, 0, 0, 0, 0, 0, 175, 0, 0, 123, 0, 0, 0, 0, 0, 0, 63, 189, 151, 0, 0, 188, 0, 0, 0, 220, 0, 245, 0, 0, 0, 0, 119, 0, 215, 111, 218, 0, 0, 0, 0, 0, 0, 0], [0, 0, 246, 125, 0, 0, 212, 0, 0, 192, 0, 0, 0, 0, 0, 0, 243, 0, 0, 0, 0, 194, 0, 0, 123, 0, 0, 0, 202, 0, 0, 156, 104, 0, 0, 0, 0, 0, 0, 185, 239, 0, 188, 248, 0, 0, 0, 0, 0, 176, 0, 0, 247, 0, 0, 0, 0, 0, 94, 0, 182, 0, 0, 0, 0, 70, 80, 0], [0, 0, 0, 0, 0, 0, 0, 144, 0, 0, 0, 0, 186, 0, 141, 0, 0, 0, 0, 86, 0, 0, 155, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 200, 0, 0, 0, 0, 212, 0, 157, 0, 0, 0, 86, 0, 0, 0, 162, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 190, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 130, 0, 0, 0, 0, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 196, 0, 0, 0, 0, 0, 0, 0, 157, 0, 0, 199, 183, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 223, 99, 0, 0, 0, 0, 187, 0, 0, 193, 0, 0, 0, 0, 0, 0, 0, 163], [0, 0, 100, 0, 0, 0, 0, 0, 0, 133, 0, 0, 0, 196, 0, 0, 170, 194, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 196, 0, 0, 209, 152, 216, 0, 0, 0, 0, 0, 0, 117, 0, 0, 193, 0, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 238, 161, 52, 0, 0, 0, 0, 214, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 162, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 200, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 169, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 217, 0, 0, 108, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 123, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 145, 0, 0, 83, 104, 0, 0, 0, 0, 0, 0, 61, 0, 0, 0, 204, 0, 0, 0, 0, 0, 0, 0, 0, 164, 242, 0, 0, 0, 0, 210, 0, 218, 0, 0, 0, 0, 54, 92, 0], [0, 0, 0, 0, 0, 0, 0, 132, 72, 0, 0, 0, 74, 198, 127, 0, 0, 0, 0, 0, 196, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 158, 97, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 52], [51, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0], [0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 0, 0, 0, 0, 235, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 135, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 148, 0, 0, 181, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 202, 0, 0, 0, 196, 0, 0, 145, 0, 0, 0, 0, 0, 0, 61, 100, 0, 0, 210, 0, 0, 0, 150, 0, 0, 0, 59, 0, 240, 0, 0, 0, 0, 0, 0, 57, 103, 0, 0, 0, 0, 0, 0, 144, 225, 0, 0, 0, 152, 223, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 166, 0, 0, 0, 0, 218, 71, 95, 0, 0, 0, 0, 175, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 213, 0, 0, 0, 0, 0, 0, 235, 56, 196, 0, 0, 0, 0, 0, 0, 0, 0, 234, 0, 0, 0, 0, 146, 0, 0, 247, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 189, 0, 0, 237, 64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 156, 0, 0, 0, 209, 0, 0, 83, 0, 0, 0, 61, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 98, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0, 91, 161, 0, 0, 0, 0, 0, 0, 163, 0, 0, 0, 0, 97, 164, 0], [0, 0, 163, 229, 0, 0, 135, 0, 0, 221, 0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 152, 0, 0, 104, 0, 0, 0, 100, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 148, 244, 0, 0, 144, 0, 216, 0, 0, 0, 0, 0, 0, 150, 200, 0, 0, 0, 0, 194, 0, 114, 0, 0, 0, 0, 74, 144, 0], [0, 0, 0, 0, 0, 0, 0, 0, 224, 163, 223, 122, 0, 214, 0, 0, 123, 0, 0, 0, 157, 216, 0, 0, 0, 0, 0, 0, 0, 0, 213, 0, 0, 0, 0, 0, 0, 0, 0, 0, 114, 192, 0, 0, 0, 190, 0, 0, 0, 0, 0, 142, 0, 0, 0, 0, 70, 0, 0, 57, 0, 0, 0, 0, 0, 0, 0, 0], [0, 227, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 235, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 201, 0, 0, 73, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 210, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 154, 0, 0, 0, 0, 0, 0, 0, 0, 198, 113, 0, 0, 0, 0, 0, 0, 0, 88, 0, 228, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 169, 0, 0, 0, 222, 0, 0, 0, 0, 0, 0, 0, 199, 0, 0, 0, 0, 158, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 111], [0, 0, 0, 0, 0, 0, 0, 229, 117, 0, 0, 0, 163, 0, 208, 0, 0, 0, 0, 0, 183, 0, 0, 0, 0, 97, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 53], [0, 0, 0, 0, 213, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 180, 0, 0, 0, 0, 0, 0, 0, 0, 95, 0, 199, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 185, 0, 0, 0, 0, 0, 0, 61, 0, 0, 0, 150, 0, 0, 98, 148, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 207, 0, 0, 0, 0, 0, 0, 0, 0, 146, 230, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 145, 0], [0, 0, 211, 0, 0, 0, 0, 0, 0, 62, 208, 146, 0, 215, 0, 0, 63, 239, 0, 0, 0, 117, 0, 0, 0, 0, 0, 0, 0, 0, 235, 0, 244, 114, 0, 0, 0, 0, 0, 0, 0, 241, 198, 0, 0, 124, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 145, 0, 237, 74, 168, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 220, 0, 0, 0, 0, 238, 122, 95, 0, 0, 0, 0, 189, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 0, 0, 192, 0, 0, 0, 0, 0, 0, 241, 0, 243, 0, 0, 0, 0, 0, 0, 0, 0, 184, 0, 0, 0, 0, 121, 237, 0, 236, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 147, 177, 0, 0, 0, 0, 137, 125, 186, 0, 0, 0, 0, 151, 188, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 196, 0, 0, 0, 0, 0, 0, 0, 0, 0, 198, 243, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 244, 0, 109, 0, 0, 0, 0, 0, 0, 0, 243, 0], [0, 0, 117, 0, 0, 139, 134, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 193, 0, 0, 204, 0, 0, 0, 59, 0, 0, 120, 144, 0, 0, 154, 0, 0, 0, 207, 0, 0, 0, 0, 0, 221, 0, 0, 0, 0, 0, 0, 80, 61, 0, 0, 0, 0, 0, 0, 142, 166, 0, 0, 0, 207, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 105, 0, 0, 0, 0, 0, 0, 167, 0, 0, 0, 126, 0, 0, 188, 0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 240, 0, 0, 0, 216, 190, 0, 0, 0, 0, 0, 0, 124, 0, 0, 221, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 133, 103, 226, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 169, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 180, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 210, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 163, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 155, 0, 0, 163, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 89, 190, 0, 0, 0, 0, 198, 185, 0, 0, 0, 0, 0, 220, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 82, 0, 0, 0, 0, 0, 0, 243, 207, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 223, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 191, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 228, 0, 0, 186, 0, 0, 0, 0, 245, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 234, 0, 0, 142, 0, 0, 0, 0, 0, 0, 0, 184, 0, 0, 0, 0, 0, 0, 0, 0, 191, 0, 0, 0, 0, 0, 129, 0, 0, 197, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 193, 0, 0, 151, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 247, 0, 0, 0, 0, 0, 0, 164, 0, 0, 0, 57, 0, 0, 91, 150, 0, 0, 198, 0, 0, 0, 146, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 200, 235, 0, 0, 0, 188, 0, 0], [0, 0, 166, 0, 0, 79, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 242, 0, 0, 0, 103, 0, 0, 161, 200, 0, 0, 113, 0, 0, 0, 230, 0, 0, 0, 61, 0, 0, 0, 0, 0, 0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 0, 202, 157, 0, 0, 0, 0, 0, 0], [0, 0, 0, 237, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 135, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 0, 0, 0, 0, 0, 0, 0, 210, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 170, 168, 64, 0, 0, 0, 0, 119, 0, 0, 0, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 0, 0, 70, 0, 0, 0, 0, 0, 0, 145, 121, 244, 0, 0, 248, 0, 0, 0, 0, 0, 129, 0, 0, 0, 0, 0, 0, 0, 118, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 199, 0, 0, 237, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 60, 0, 0, 0, 0, 0, 176, 234, 0, 0, 0, 0, 0, 215, 94, 0, 0, 0, 238, 0, 0, 210, 0, 0, 0, 0, 0, 0, 0, 194, 0, 0, 0, 0, 0, 0, 0, 237, 0, 109, 0, 0, 0, 0, 0, 0, 82, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 245, 0, 0, 0, 0, 161, 134, 0], [0, 0, 237, 0, 0, 0, 0, 0, 228, 134, 242, 152, 0, 174, 0, 0, 111, 0, 0, 0, 193, 161, 0, 0, 0, 0, 0, 0, 0, 0, 247, 0, 0, 57, 0, 0, 0, 0, 0, 0, 74, 236, 0, 0, 0, 133, 0, 0, 0, 0, 0, 197, 0, 0, 0, 0, 118, 0, 0, 0, 213, 0, 0, 0, 0, 0, 0, 0], [0, 0, 69, 0, 0, 0, 219, 0, 0, 175, 0, 0, 0, 221, 0, 0, 218, 182, 0, 0, 0, 52, 0, 0, 218, 0, 0, 0, 144, 0, 0, 163, 114, 0, 0, 0, 0, 0, 0, 0, 168, 0, 0, 142, 0, 103, 0, 0, 0, 0, 0, 0, 200, 202, 0, 0, 0, 0, 245, 213, 0, 222, 0, 0, 0, 185, 247, 0], [0, 0, 153, 0, 0, 154, 0, 0, 0, 0, 0, 0, 0, 223, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 225, 0, 0, 0, 0, 0, 0, 88, 0, 0, 0, 0, 0, 0, 0, 166, 0, 226, 0, 0, 0, 0, 0, 0, 235, 157, 0, 0, 0, 0, 0, 0, 222, 0, 0, 153, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 136, 0, 0, 0, 0, 207, 183, 187, 0, 0, 0, 104, 190, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 228, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 153, 0, 0, 0, 0, 0, 0], [56, 127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 143, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 237, 178, 0, 0, 145, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0, 214, 0, 0, 54, 0, 0, 0, 152, 0, 0, 97, 74, 0, 0, 0, 0, 0, 0, 115, 0, 0, 0, 207, 0, 0, 0, 0, 0, 243, 0, 0, 188, 0, 0, 0, 0, 0, 161, 0, 185, 0, 0, 0, 0, 0, 71, 0], [0, 0, 0, 127, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 92, 0, 0, 0, 223, 0, 0, 164, 144, 0, 0, 0, 0, 0, 0, 145, 0, 0, 243, 0, 0, 0, 0, 0, 0, 207, 0, 0, 0, 0, 0, 0, 0, 0, 134, 0, 247, 0, 0, 0, 0, 71, 0, 0], [0, 0, 0, 0, 0, 0, 0, 184, 67, 0, 0, 0, 125, 229, 177, 0, 0, 0, 0, 0, 163, 0, 0, 0, 0, 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 111, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
min_cover(ma)