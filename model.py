import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._artObjectList = DAO.getAllObjects()
        self._grafo = nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)
        self._idMap = {}
        for v in self._artObjectList:
            self._idMap[v.object_id] = v

        self._solBest = []
        self._pesoBest = 0


    def creaGrafo(self):
        self.addEdges()


    def addEdges(self):
        self._grafo.clear_edges()


        # Soluzione1: ciclare sui nodi
        #for u in self._artObjectList:
        #    for v in self._artObjectList:
        #        peso = DAO.getPeso(u,v)
        #        self._grafo.add_edge(u, v, weight=peso)

        # Soluzione2: una sola query
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def checkExistence(self, idOgetto):
        return idOgetto in self._idMap  # True o False a seconda se esiste o meno l'id dell'oggetto passato

    def getConnessa(self, v0int):
        v0 = self._idMap[v0int]

        # Modo 1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0) # definisce i successori nel grafo dell'oggetto passato
        allSucc = []
        for v in successors.values():
            allSucc.extend(v)
            # extend funziona come append, ma al posto di aspettarsi un oggetto, questo fa l'unpack di v

        print(f"Metodo 1 (succ): {len(allSucc)}")

        # Modo 2: predecessori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"Metodo 2 (pred): {len(predecessors.values())}")

        # Modo 3: conto i nodi dell'albero in visita
        tree = nx.dfs_tree(self._grafo, v0)
        print(f"Metodo 3 (tree): {len(tree.nodes)}")

        # Modo 4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)
        print(f"Metodo 4 (connected component): {len(connComp)}")
        return len(connComp)

    def getObjFromId(self, oggetto):
        return self._idMap[int(oggetto)]

    def getBestPath(self, lun, v0):
        self._solBest = []
        self._pesoBest = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

        return self._solBest, self._pesoBest


    def ricorsione(self, parziale, lun):

        # 1. controllo se parziale è una soluzione valida ed in caso se è migliore del best
        if len(parziale) == lun:
            if self.peso(parziale) > self._pesoBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return


        # 2. ricorsione
        # se arrivo qui allora len(parziale) < lun
        for v in self._grafo.neighbors(parziale[-1]):
            # v lo aggiungo se non è già in parziale e se ha stessa classification di v0
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()



    def peso(self, listObject):
        p = 0
        for i in range(0, len(listObject)-1):
            p += self._grafo[listObject[i]][listObject[i+1]]["weight"]

        return p