import numpy as np
import math as mt
import pandas as pd
from scipy.stats import qmc


class Parameters:

    def __init__(self, number_of_nodes):

        # Default input cooperativity
        self.n_i_default = 1
        # Default input activation threshold
        self.k_i_default = 0.4

        # Input cooperativity sampling range
        # **********************************
        self.n_i_lower = 1
        self.n_i_upper = 4

        # Input activation threshold sampling range
        # **********************************
        self.k_i_lower = 0.001
        self.k_i_upper = 1

        # Protein degradation rate sampling range
        self.tau_lower = 1
        self.tau_upper = 100

        # Activation/inhibition threshold sampling range
        self.K_lower = 0.001
        self.K_upper = 1

        # Cooperativity sampling range
        self.n_lower = 1
        self.n_upper = 4

        # Number of nodes in the network
        self.number_of_nodes = number_of_nodes

        # Label for input to network
        self.input = 'I'
        # Label for input cooperativity
        self.n_i = 'nI'
        # Label for input activation threshold
        self.k_i = 'KI'

        self.x = []
        self.v = []
        self.tau = []

        # Shape of adjacency matrix of the network
        shape = (number_of_nodes, number_of_nodes)

        # Get the shape of activation/inhibition threshold matrix based on shape of adjacency matrix
        self.K = np.ndarray(shape, dtype='object')
        # Get the shape of cooperativities matrix based on shape of adjacency matrix
        self.n = np.ndarray(shape, dtype='object')

        for i in range(number_of_nodes):
            # Get labels for concentration of each node in the network
            self.x.append('x[' + str(i) + ']')
            # Get labels for maximal production rate of each node in the network
            self.v.append('v' + str(i))
            # Get degradation rate of each node in the network
            self.tau.append('tau' + str(i))
            for j in range(number_of_nodes):
                # Get labels for activation/inhibition threshold for all possible edges in the network
                self.K[i][j] = str('K' + str(i) + '_' + str(j))
                # Get labels for cooperativities for all possible edges in the network
                self.n[i][j] = str('n' + str(i) + '_' + str(j))

    def sample_parameters_lhs(self, nsamples):

        samples_dict = {}

        # Input cooperativity - We take the default instead of sampling
        n_i = self.n_i_default
        n_i = np.repeat(n_i, nsamples)
        samples_dict[self.n_i] = n_i

        # Input activation threshold - We take the default instead of sampling
        k_i = self.k_i_default
        k_i = np.repeat(k_i, nsamples)
        samples_dict[self.k_i] = k_i

        # Dimension of parameter space for non-dimensionalised model where v is just a variable equal to 1/tau
        # 'tau': number of nodes, 'K': number of nodes*number of nodes, 'n': number of nodes*number of nodes
        dimension = self.number_of_nodes + 2*(self.number_of_nodes*self.number_of_nodes)

        sampler = qmc.LatinHypercube(d=dimension)
        sample_unscaled = sampler.random(n=nsamples)
        low = []
        for i in range(self.number_of_nodes):
            low.append(mt.log10(self.tau_lower))
        for i in range(self.number_of_nodes*self.number_of_nodes):
            low.append(mt.log10(self.K_lower))
        for i in range(self.number_of_nodes * self.number_of_nodes):
            low.append(self.n_lower)

        high = []
        for i in range(self.number_of_nodes):
            high.append(mt.log10(self.tau_upper))
        for i in range(self.number_of_nodes * self.number_of_nodes):
            high.append(mt.log10(self.K_upper))
        for i in range(self.number_of_nodes * self.number_of_nodes):
            high.append(self.n_upper)

        sample = qmc.scale(sample_unscaled, low, high)
        sample[:, 0:12] = 10 ** (sample[:, 0:12])

        tau = sample[:, 0:3]
        v = np.reciprocal(tau)
        K = sample[:, 3:12]
        K = K.reshape(nsamples, self.number_of_nodes, self.number_of_nodes)
        n = sample[:, 12:]
        n = n.reshape(nsamples, self.number_of_nodes, self.number_of_nodes)

        # Consider only integral values of cooperativity
        n = np.round(n, decimals=0)

        # Get the samples generated into dictionary
        # *************************************************
        for i in range(self.number_of_nodes):
            samples_dict[self.v[i]] = [row[i] for row in v]
            samples_dict[self.tau[i]] = [row[i] for row in tau]

        for row in range(self.number_of_nodes):
            for col in range(self.number_of_nodes):
                samples_dict[self.K[row, col]] = [val[row, col] for val in K]
                samples_dict[self.n[row, col]] = [val[row, col] for val in n]

        # *************************************************
        # Get samples dictionary into a dataframe
        df_samples = pd.DataFrame(samples_dict)

        return df_samples

    def sample_initial_conditions_lhs(self, nsamples):

        samples_dict = {}
        dimension = self.number_of_nodes
        sampler = qmc.LatinHypercube(d=dimension)
        sample_unscaled = sampler.random(n=nsamples)
        low = [mt.log10(0.001), mt.log10(0.001), mt.log10(0.001)]
        high = [mt.log10(1), mt.log10(1), mt.log10(1)]
        x = 10 ** qmc.scale(sample_unscaled, low, high)

        # Get the samples generated into dictionary
        for i in range(self.number_of_nodes):
            samples_dict[self.x[i]] = [row[i] for row in x]

        # Get samples dictionary into a dataframe
        df_sample_ics = pd.DataFrame(samples_dict)

        return df_sample_ics

    def get_network_as_dataframe(self, adj_matrix, nparams):

        # All the parameters simulated are for a particular network given by
        # the adjacency matrix. So repeat the adjacency matrix by the number
        # of parameters for which the simulation has been done
        flat_adj_matrix_index = []
        flat_adj_matrix = np.repeat([adj_matrix], nparams, axis=0)

        for p in range(self.number_of_nodes):
            for q in range(self.number_of_nodes):
                flat_adj_matrix_index = flat_adj_matrix_index + ['Adj' + str(p) + '_' + str(q)]

        df_network = pd.DataFrame(data=flat_adj_matrix, columns=flat_adj_matrix_index)
        return df_network

    def make_unnecessary_params_zero(self, df):

        # If an adjacency matrix element [i, j] is zero. i.e., an edge is absent, make the parameters
        # (Ki_j, ni_j) in the parameter sets corresponding to that edge zero

        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                for itern in range(len(df['Adj' + str(i) + '_' + str(j)])):
                    if df['Adj' + str(i) + '_' + str(j)][itern] == 0:
                        df.loc[itern, 'K' + str(i) + '_' + str(j)] = 0
                        df.loc[itern, 'n' + str(i) + '_' + str(j)] = 0
        return df
