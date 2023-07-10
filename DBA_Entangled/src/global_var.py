import numpy as np
# Global variable to store experiment data for data collection or debugging purposes
# import main

# Initialize global variable
global_list = np.full((1,1),999, dtype='i')
global_basis = np.full((1,1),999, dtype='i')
global_basis_sum = np.full((1,1),999, dtype='i')
sum = 0 # value to save round number

# Function to resize global variable
def resize(m,n):
    global global_list
    global global_basis
    global global_basis_sum
    global_list = np.resize(global_list,(m,n))
    global_basis = np.resize(global_basis,(m,n))
    global_basis_sum = np.resize(global_basis_sum,(m,n))

# Function to modify the global array value

def modify_sum():
    global sum
    sum = sum+1


def modify_sum_var(n):
    global sum
    sum = n
    
def modify(value,i,j):
    # print("From global_var function:")
    global global_list
    global_list[i][j] = value

def modify_basis(value,i,j):
    global global_basis
    global_basis[i][j] = value


def modify_basis_sum(value,i,j):
    global global_basis_sum
    global_basis_sum[i][j] = value