import pandas as pd
import numpy as np
from itertools import combinations

class network:
    """Defines input as network
    """
    def __init__(self, Adjacency_Matrix):
        assert isinstance(Adjacency_Matrix, pd.DataFrame), "Input must be panda.DataFrame"
        self.adj_mat=Adjacency_Matrix
        self.nodes = list(self.adj_mat.index)
    def degree(self, node="all"):
        """
        Calculate the degree of each node in the network and saves it as pd.Series
        """
        return self.adj_mat.sum(axis=1)-1

    def shortestpath(self):
        """
        Calculate the shortest path between all nodes in the network using Dijstrak Algorithm
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        inv_adj_mat=self.adj_mat.abs().pow(-1)                                                                          # Inverts adjacency matrix
        shortestpath_df=pd.DataFrame(np.zeros(inv_adj_mat.shape), columns=self.nodes, index=self.nodes)                # Initialize
        counter=0
        for n in self.nodes:
            node_set=pd.DataFrame({'Distance': np.full((len(self.nodes)-counter), np.inf), 'Previous': ['']*(len(self.nodes)-counter)}, index=self.nodes[n:])
            node_set.loc[n, 'Distance'] = 0
            unvisited_nodes=self.nodes[n:]
            while unvisited_nodes != []:
                current=node_set.loc[unvisited_nodes,'Distance'].idxmin()    # Select node with minimal Distance of the unvisited nodes
                unvisited_nodes.remove(current)
                for k in range(n, len(self.nodes)):
                    dist=node_set.loc[current, 'Distance'] + inv_adj_mat.loc[current, k]
                    if node_set.loc[k, 'Distance'] > dist:
                        node_set.loc[k,'Distance'] = dist
                        node_set.loc[k, 'Previous'] = current
            shortestpath_df.iloc[n:,n]=node_set.loc[:,'Distance']
            shortestpath_df.iloc[n, n:]=node_set.loc[:,'Distance']
            counter += 1
        return shortestpath_df

    def num_triangles(self):
        triangles=pd.Series(np.zeros(len(self.nodes)), index=self.nodes)
        all_combinations=combinations(self.nodes, 3)    # Create list of all possible triangles
        abs_adj_mat = self.adj_mat.abs()
        sum_dict={}
        for comb in all_combinations:
            n1_n2=abs_adj_mat.loc[comb[0],comb[1]]
            n1_n3=abs_adj_mat.loc[comb[0],comb[2]]
            n2_n3=abs_adj_mat.loc[comb[1],comb[2]]
            sum_dict[comb]=(n1_n2+n1_n3+n2_n3)**(1/3)   # Calculate the triangle sum of the combination and save it in dictionary
        for node in self.nodes:
            triangles[node]=0.5*np.sum([sum_dict[s] for s in sum_dict if node in s])    # Sum all of the triangles that contain the node
        return triangles

    def char_path(self):
        sum_shrtpath_df=self.shortestpath().sum(axis=1)     # Sums Shortest Path Dataframe along axis 1
        avg_shrtpath=np.divide(sum_shrtpath_df, len(self.nodes)-1)  # Divide each element in sum array by n-1 regions
        return np.sum(avg_shrtpath)/len(self.nodes)                 # Calculate sum of the sum array and take the average

    def glob_efficiency(self):
        inv_shrtpath=self.shortestpath().pow(-1)                    # Takes the inverse of each element of the Dataframe
        for n in self.nodes: inv_shrtpath.loc[n,n]=0                # Set Diagonal from inf -> 0
        sum_invpath_df=inv_shrtpath.sum(axis=1)                     # Sums Shortest Path Dataframe along axis 1
        avg_invpath=np.divide(sum_invpath_df, len(self.nodes)-1)    # Divide each element in sum array by n-1 regions
        return np.sum(avg_invpath)/len(self.nodes)                 # Calculate sum of the sum array and take the average
