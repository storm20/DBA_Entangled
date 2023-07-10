import cmath
import numpy as np


# Custom Operator in matrix form for U and V gate


def UOperator(num_parties):
        basis_matrix = np.identity(num_parties)
        z = cmath.exp((2*np.pi/num_parties)*1j)
        U = basis_matrix[:,0].reshape(num_parties,1)*np.transpose(basis_matrix[:,0].reshape(num_parties,1))
        i = 1
        while i< num_parties:
            U = U +  z*(basis_matrix[:,i].reshape((num_parties,1))*np.transpose(basis_matrix[:,i].reshape(num_parties,1)))
            i= i+1
        return U
    
def VOperator(num_parties):
    basis_matrix = np.identity(num_parties)
    V = np.zeros(num_parties)
    z = cmath.exp((2*np.pi/num_parties)*1j)
    for i in range(num_parties):
        V = V + (z**i)*(basis_matrix[:,i].reshape((num_parties,1))*np.transpose(basis_matrix[:,i].reshape(num_parties,1)))
    return V
