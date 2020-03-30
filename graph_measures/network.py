import pandas as pd
import numpy as np
from itertools import combinations
from Graph_measures import functions as func

class network:
    """Defines input as network
    :parameter pd.DataFrame that contains the adjacency matrix of the network, np.ndarray timecourse matrix
    """
    def __init__(self, Adjacency_Matrix, tc):
        assert isinstance(Adjacency_Matrix, pd.DataFrame), "Input must be panda.DataFrame"
        self.adj_mat=Adjacency_Matrix
        self.nodes = list(self.adj_mat.index)

        assert isinstance(tc, np.ndarray), "Timecourse must be np.ndarray"
        self.cov_mat=func.covariance_mat(tc)

    def degree(self, node="all"):
        """
        Calculate the degree of each node in the network.
        :return n dimensional pd.Series with degrees of all nodes in the network
        """
        return self.adj_mat.sum(axis=1)-1

    def shortestpath(self):
        """
        Calculate the shortest path between all nodes in the network using Dijstrak Algorithm:
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        :return Dictionary of two nxn dimensional pd.DataFrames with shortest path / shortest distance between all pairs of nodes in the network
        """
        inv_adj_mat=self.adj_mat.abs().pow(-1)                                                                          # Inverts adjacency matrix
        shortestdist_df=pd.DataFrame(np.zeros(inv_adj_mat.shape), columns=self.nodes, index=self.nodes)                 # Initialize Path matrix and distance matrix
        shortestpath_df=pd.DataFrame(np.empty(inv_adj_mat.shape, dtype=str), columns=self.nodes, index=self.nodes)
        counter=0
        for n in range(len(self.nodes)):
            node_set=pd.DataFrame({'Distance': np.full((len(self.nodes)-counter), np.inf),
                                   'Previous': ['']*(len(self.nodes)-counter), 'Path': ['']*(len(self.nodes)-counter)}, index=self.nodes[n:])
            node_set.loc[self.nodes[n], 'Distance'] = 0
            unvisited_nodes=self.nodes[n:]
            while unvisited_nodes != []:
                current=node_set.loc[unvisited_nodes,'Distance'].idxmin()    # Select node with minimal Distance of the unvisited nodes
                unvisited_nodes.remove(current)
                for k in self.nodes[n:]:
                    dist=node_set.loc[current, 'Distance'] + inv_adj_mat.loc[current, k]
                    if node_set.loc[k,'Distance'] > dist:
                        node_set.loc[k,'Distance'] = dist
                        node_set.loc[k,'Previous'] = current
            shortestdist_df.loc[n:,n]=node_set.loc[:,'Distance']
            shortestdist_df.loc[n, n:]=node_set.loc[:,'Distance']
            # Create Dataframe with string values for the shortest path between each pair of nodes
            for k in self.nodes[n:]:
                path=str(k)
                current=k
                while node_set.loc[current, 'Previous'] != '':
                    current=node_set.loc[current, 'Previous']
                    path=str(current)+'-'+path
                node_set.loc[k,'Path']=path
            shortestpath_df.loc[n:,n]=node_set.loc[:,'Path']
            shortestpath_df.loc[n,n:]=node_set.loc[:,'Path']
            counter += 1
        return {'Distance': shortestdist_df, 'Path': shortestpath_df}

    def num_triangles(self):
        """
        Calculate sum of triangles edge weights around each node in network
        :return: n dimensional pd.Series
        """
        triangles=pd.Series(np.zeros(len(self.nodes)), index=self.nodes)
        all_combinations=combinations(self.nodes, 3)        # Create list of all possible triangles
        abs_adj_mat = self.adj_mat.abs()
        sum_dict={}
        for combi in all_combinations:
            n1_n2=abs_adj_mat.loc[combi[0],combi[1]]        # Get path length between pairs in triangle combination
            n1_n3=abs_adj_mat.loc[combi[0],combi[2]]
            n2_n3=abs_adj_mat.loc[combi[1],combi[2]]
            sum_dict[combi]=(n1_n2+n1_n3+n2_n3)**(1/3)       # Calculate the triangle sum of the combination and save it in dictionary
        for node in self.nodes:
            triangles[node]=0.5*np.sum([sum_dict[s] for s in sum_dict if node in s])    # Sum all of the triangles that contain the node
        return triangles

    def char_path(self):
        """
        Calculate the characteristic path length of the network
        :return: Dictionary with average node distance np.array and characteristic path length np.float object
        """
        sum_shrtpath_df=self.shortestpath().sum(axis=1)             # Sums Shortest Path Dataframe along axis 1
        avg_shrtpath_node=np.divide(sum_shrtpath_df, len(self.nodes)-1)  # Divide each element in sum array by n-1 regions
        char_pathlength=np.sum(avg_shrtpath_node)/len(self.nodes)
        return {'node_avg_dist':avg_shrtpath_node, 'characteristic_path': char_pathlength}    # Calculate sum of the sum array and take the average

    def glob_efficiency(self):
        """
        Calculate the global efficiency of the network
        :return: np.float object
        """
        inv_shrtpath=self.shortestpath().pow(-1)                    # Takes the inverse of each element of the Dataframe
        for n in self.nodes: inv_shrtpath.loc[n,n]=0                # Set Diagonal from inf -> 0
        sum_invpath_df=inv_shrtpath.sum(axis=1)                     # Sums Shortest Path Dataframe along axis 1
        avg_invpath=np.divide(sum_invpath_df, len(self.nodes)-1)    # Divide each element in sum array by n-1 regions
        return pd.Series(np.sum(avg_invpath)/len(self.nodes), index=self.nodes)                  # Calculate sum of the sum array and take the average

    def clust_coeff(self):
        """
        Calculate the cluster coefficient of the network
        :return: Dictionary of network cluster coefficient np.float object and ndim np.array of node cluster coefficients
        """
        triangles=np.multiply(np.array(self.num_triangles()), 2)
        degrees=np.array(self.degree())
        excl_nodes=np.where(degrees < 2); triangles[excl_nodes]=0
        degrees=np.multiply(degrees, degrees-1)
        node_clust=np.divide(triangles,degrees)
        net_clust=(1/len(self.nodes))*np.sum(node_clust)
        return {'node_cluster':pd.Series(node_clust, index=self.nodes), 'net_cluster':net_clust}

    def transitivity(self):
        """
        Calculate the transitivity of the network
        :return: np.float
        """
        triangles=np.sum(np.multiply(np.asarray(self.num_triangles()),2))     # Multiply sum of triangles with 2 and sum the array
        degrees=np.array(self.degree())
        degrees=np.sum(np.multiply(degrees, degrees-1))
        return np.divide(triangles, degrees)

    def closeness_centrality(self):
        """
        Calculate the closeness centrality of each node in network
        :return: ndimensional pd.Series
        """
        node_avg_distance=self.char_path()['node_avg_dist']
        return pd.Series(np.power(node_avg_distance, -1), index=self.nodes)

    def betweenness_centrality(self):
        """
        Calculate the betweenness centrality of each node in network
        :return: ndimensional pd.Series
        """
        betw_centrality=pd.Series(np.zeros(len(self.nodes)), index=self.nodes)
        shortest_paths=self.shortestpath()['Path']
        for n in self.nodes:
            counter = 0
            mat=shortest_paths.drop(n, axis=0); mat=mat.drop(n, axis=1)  # Drops the nth column and the nth row.
            substr='-'+str(n)+'-'
            for c in mat.columns:
                for e in mat.loc[:c,c]:
                    if e.find(substr) != -1:
                        counter += 1
            betw_centrality.loc[n]=counter/((len(self.nodes)-1)*(len(self.nodes)-2))
        return betw_centrality

    def random_net(self):
        """
        Returns a random network that is matched to the input networks covariance matrix.
        Using Hirschberger-Qi-Steuer Algorithm as cited in Zalesky 2012b
        :return: n x n dimensional pd.Dataframe
        TODO test code, control if input has to be is positive finite
        """
        C=self.cov_mat
        diag_sum=np.sum(np.diagonal(C))
        diag_len=len(np.diagonal(C))
        diag_mean=diag_sum/diag_len
        off_mean=(np.sum(C)-diag_sum)/(C.size-diag_len)
        off_var=0
        for i in range(0,C.shape(0)-1):
            for j in range(i+1,C.shape(1)):
                off_var += 2*(C[i,j]-off_mean)  # Times 2  because each off diagonal value appears twice in covariance matrix
        m = max(2, (diag_mean**2-off_mean**2/off_var))
        mu = np.sqrt(off_mean/off_var)
        sigma = -mu**2 + np.sqrt(mu**4+(off_var/m))
        X=np.random.normal(mu,sigma,C.size)
        Random_C=np.multiply(X,X.T)
        return Random_C

    def assortivity(self):
        return
    def smallworldness(self):
        return
