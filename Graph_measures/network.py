import pandas as pd
import numpy as np
from pandas import DataFrame

class network:
    """Defines input as network
    """
    def __init__(self, Adjacency_Matrix):
        assert isinstance(Adjacency_Matrix, pd.DataFrame), "Input must be panda.DataFrame"
        self.nodes=list(Adjacency_Matrix.index)
        self.adj_mat=Adjacency_Matrix
    def degree(self, node="all"):
        """
        Calculate the degree of each node in the network and saves it as pd.Series
        """
        return self.adj_mat.sum(axis=1)-1
    def shortestpath(self):
        """
        Calculate the shortest path between all nodes in the network using the Dijstrak Algorithm
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        print('Calculate shortest path length matrix')
        inv_adj_mat=self.adj_mat.abs().pow(-1)                                                                          # Inverts adjacency matrix
        shortestpath_mat=pd.DataFrame(np.zeros(inv_adj_mat.shape), columns=self.nodes, index=self.nodes)                # Initialize
        counter=0
        for n in self.nodes:
            node_set=pd.DataFrame({'Distance': np.full((len(self.nodes)-counter), np.inf), 'Previous': ['']*(len(self.nodes)-counter)}, index=self.nodes[n:])
            node_set.loc[n, 'Distance'] = 0
            unvisited_nodes=self.nodes[n:]
            counter += 1
            while unvisited_nodes != []:
                current=node_set.loc[unvisited_nodes,'Distance'].idxmin()    # Select node with minimal Distance of the unvisited nodes
                unvisited_nodes.remove(current)
                for k in range(n, len(self.nodes)):
                    dist=node_set.loc[current, 'Distance'] + inv_adj_mat.loc[current, k]
                    if node_set.loc[k, 'Distance'] > dist:
                        node_set.loc[k,'Distance'] = dist
                        node_set.loc[k, 'Previous'] = current
            shortestpath_mat.iloc[n:,n]=node_set.loc[:,'Distance']
            shortestpath_mat.iloc[n, n:]=node_set.loc[:,'Distance']
        return shortestpath_mat