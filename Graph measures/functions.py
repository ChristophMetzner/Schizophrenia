import numpy as np
import math
from scipy import stats

def pearson_corr(M):
    """ Returns the pearson correlation coefficients between pairs of rows in M.
        The function uses matrix inversion to calculate the partial correlation.

        Parameters:
             M : array-like, shape (n, p)
            Array with the different variables. Each row of M is taken as a variable

        Returns:
            P : array-like, shape (n, n)
            P[i, j] contains the partial correlation of M[i, :] and M[j, :] controlling
            for the remaining variables in M.
        """
    P=np.array([np.corrcoef((M[i,:], M[j,:]))[0,1] for i in range(M.shape[0]) for j in range(M.shape[0])])
    return P.reshape(M.shape[0],M.shape[0])

def partial_corr_inv(M):
    """ Returns the partial linear correlation coefficients between pairs of rows in M.
    The function uses matrix inversion to calculate the partial correlation.

    Parameters:
         M : array-like, shape (n, p)
        Array with the different variables. Each row of M is taken as a variable

    Returns:
        P : array-like, shape (n, n)
        P[i, j] contains the partial correlation of M[i, :] and M[j, :] controlling
        for the remaining variables in M.
    """

    inv_M=np.linalg.inv(pearson_corr(M))
    P=np.array([-(inv_M[i,j])/math.sqrt(inv_M[i,i]*inv_M[j,j]) for i in range(inv_M.shape[0]) for j in range(inv_M.shape[0])])
    P=P.reshape(inv_M.shape)        #reshaping the 1x(p^2) dimensional array to a pxp dimensional array
    return np.fill_diagonal(P,1)    #fill diagonal with ones and return matrix

def partial_corr(M):
    """ Returns the partial linear correlation coefficients between pairs of rows in M.
    The function uses matrix inversion to calculate the partial correlation.

    Parameters:
         M : array-like, shape (n, p)
        Array with the different variables. Each row of M is taken as a variable

    Returns:
        P : array-like, shape (n, n)
        P[i, j] contains the partial correlation of M[i, :] and M[j, :] controlling
        for the remaining variables in M.
    """
    M=np.asarray(M).T
    part_corr = np.eye(M.shape[1], dtype=np.float)
    M=np.concatenate((M,np.ones((M.shape[0],1))), 1)
    for i in range(M.shape[1]-1):
        for j in range(i+1, M.shape[1]-1):
            idx=np.ones(M.shape[1], dtype=np.bool)
            idx[[i,j]]=False
            beta_i = np.linalg.lstsq(M[:, idx], M[:, i], rcond=None)[0]
            beta_j = np.linalg.lstsq(M[:, idx], M[:, j], rcond=None)[0]

            res_i = M[:, i] - M[:, idx].dot(beta_i)
            res_j = M[:,j] - M[:, idx].dot(beta_j)

            corr = np.corrcoef(res_i, res_j)[0,1]
            part_corr[i,j]=corr
            part_corr[j,i]=corr
    return part_corr


