import numpy as np
from itertools import product

def generate_all_nxn_adjacency_matrices(number_of_rows):

    # Shape of adjacency matrix: (n x n)
    shape_of_adj_matrix = (number_of_rows, number_of_rows)

    # Number of elements in the adjacency matrix = n*n
    no_of_elements = number_of_rows * number_of_rows

    # Elements of the adjacency matrices:
    #  0: No connection
    #  1: Activation
    # -1: Repression
    # options = [-1, 0, 1] hence selecting range(-1, 2)

    tup_mat_entries = []
    for p in product(range(-1, 2), repeat=no_of_elements):
        tup_mat_entries.append(p)
    all_mat_entries = np.array([mat for mat in tup_mat_entries])
    adj_mat_list = np.array([mat.reshape(shape_of_adj_matrix) for mat in all_mat_entries])

    return adj_mat_list

def filter_adjacency_matrices(adjacency_matrix_list):

    # Given a list of 3 by 3 adjacency matrices, this
    # function removes all those adjacency matrices
    # that have no direct or indirect connection from
    # the input node (A) to the output node (C), and
    # returns the resulting list of adjacency matrices

    index = []
    i = 0
    count = 0
    invalid_adjacency_matrix_list = []
    for adjacency_matrix in adjacency_matrix_list:
        i += 1

        row1 = adjacency_matrix[0]
        row2 = adjacency_matrix[1]
        if row1[1] == 0 and row1[2] == 0:
            count += 1
            invalid_adjacency_matrix_list.append(adjacency_matrix)
            index.append(i-1)
        elif row1[1] != 0 and row1[2] == 0 and row2[2] == 0:
            count += 1
            invalid_adjacency_matrix_list.append(adjacency_matrix)
            index.append(i - 1)

    adjacency_matrix_list = np.delete(adjacency_matrix_list, index, axis=0)
    return adjacency_matrix_list
