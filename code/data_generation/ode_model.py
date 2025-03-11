import numpy as np
import pandas as pd
from parameters import Parameters as Pr
from collections import OrderedDict
from scipy.integrate import odeint
from three_node_models import *


class OdeModel:

    def __init__(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.logic = 'AND'

    def get_model(self):
        params = Pr(len(self.adj_matrix))
        eq_dict = OrderedDict()

        if self.logic == 'AND':
            # Interaction between nodes i and j
            for i in range(len(self.adj_matrix)):
                if i == 0:
                    # Input term
                    eq_0 = "params['" + str(params.v[i]) + "'] * (" + str(params.input) + " ** params['" + str(
                        params.n_i) + "'])/(" + str(params.input) + " ** params['" + str(
                        params.n_i) + "'] + params['" + params.k_i + "'] ** params['" + str(params.n_i) + "'])"

                eq_n = "params['" + str(params.v[i]) + "']"
                for j in range(len(self.adj_matrix)):
                    # Input node: Node 0
                    if i == 0:
                        # Input term
                        if self.adj_matrix[j][i] == 1:
                            # Activation terms
                            eq_0 += " * (" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + "'])/(" + \
                                    str(params.x[j]) + " ** params['" + str(params.n[i][j]) + "'] + params['" + \
                                    params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        elif self.adj_matrix[j][i] == -1:
                            # Inhibition terms
                            eq_0 += " * ( params['" + str(params.K[i][j]) + "'] ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        if j == len(self.adj_matrix) - 1:
                            # Decay term
                            eq_0 += " - " + str(params.x[i]) + "/ params['" + str(params.tau[i]) + "']"
                            eq_dict["dot_" + params.x[i]] = eq_0

                    # Intermediate nodes and output node
                    else:
                        if self.adj_matrix[j][i] == 1:
                            # Activation terms
                            eq_n += " * (" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        elif self.adj_matrix[j][i] == -1:
                            # Inhibition terms
                            eq_n += " * (params['" + str(params.K[i][j]) + "'] ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        if j == len(self.adj_matrix) - 1:
                            eq_n += " - " + str(params.x[i]) + "/ params['" + str(params.tau[i]) + "']"
                            eq_dict["dot_" + params.x[i]] = eq_n

        return eq_dict

    def get_non_dimensionalised_model(self):
        params = Pr(len(self.adj_matrix))
        eq_dict = OrderedDict()

        if self.logic == 'AND':
            # Interaction between nodes i and j
            for i in range(len(self.adj_matrix)):
                if i == 0:
                    # Input term
                    eq_0 = "1 / params['" + str(params.tau[i]) + "'] * (" + str(params.input) + " ** params['" + str(
                        params.n_i) + "'])/(" + str(params.input) + " ** params['" + str(
                        params.n_i) + "'] + params['" + params.k_i + "'] ** params['" + str(params.n_i) + "'])"

                eq_n = "1 / params['" + str(params.tau[i]) + "']"

                for j in range(len(self.adj_matrix)):
                    # Input node: Node 0
                    if i == 0:
                        # Input term
                        if self.adj_matrix[j][i] == 1:
                            # Activation terms
                            eq_0 += " * (" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + "'])/(" + \
                                    str(params.x[j]) + " ** params['" + str(params.n[i][j]) + "'] + params['" + \
                                    params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        elif self.adj_matrix[j][i] == -1:
                            # Inhibition terms
                            eq_0 += " * ( params['" + str(params.K[i][j]) + "'] ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        if j == len(self.adj_matrix) - 1:
                            # Decay term
                            eq_0 += " - " + str(params.x[i]) + "/ params['" + str(params.tau[i]) + "']"
                            eq_dict["dot_" + params.x[i]] = eq_0

                    # Intermediate nodes and output node
                    else:
                        if self.adj_matrix[j][i] == 1:
                            # Activation terms
                            eq_n += " * (" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        elif self.adj_matrix[j][i] == -1:
                            # Inhibition terms
                            eq_n += " * (params['" + str(params.K[i][j]) + "'] ** params['" + str(params.n[i][j]) + \
                                    "'])/(" + str(params.x[j]) + " ** params['" + str(params.n[i][j]) + \
                                    "'] + params['" + params.K[i][j] + "'] ** params['" + str(params.n[i][j]) + "'])"

                        if j == len(self.adj_matrix) - 1:
                            eq_n += " - " + str(params.x[i]) + "/ params['" + str(params.tau[i]) + "']"
                            eq_dict["dot_" + params.x[i]] = eq_n

        return eq_dict

def solve_ode(model1, initial_concentrations, params, I, time_start, time_end, time_steps, paramid, ss_check):

    model = globals()[model1]
    skip = 0

    t = np.linspace(time_start, time_end, int(((time_end - time_start)/time_steps))+1)

    if ss_check == 0:
        x = initial_concentrations
        concentrations = odeint(model, x, t, args=(I, params))
        if np.any(np.isnan(concentrations)) or (concentrations<0).any():
            skip = 1
    else:
        max_iter = 10
        nrun = 1
        if all(ic > 0.001 for ic in initial_concentrations):
            x = initial_concentrations
        else:
            # Initialize at the lower bound
            x = [0.001, 0.001, 0.001]
        concentrations = odeint(model, x, t, args=(I, params))
        delta = pd.DataFrame(concentrations[-6:])
        delta = delta.pct_change(axis=1)

        # While the percentage changes in concentrations between consecutive time points in the last 5 time points
        # are greater than 1% , continue simulating and looking for steady state
        while ((abs(delta.iloc[:, 1:].values) > 0.05).any()):
            if nrun < max_iter:
                concentrations = odeint(model, concentrations[-1], t, args=(I, params))
                delta = pd.DataFrame(concentrations[-6:])
                delta = delta.pct_change(axis=1)
                nrun += 1
            else:
                break

        if (abs(delta.iloc[:, 1:].values) <= 0.05).all():
            if (concentrations[-1] > 0.001).all():
                return concentrations[-1], skip
            else:
                skip = 1
        elif nrun == max_iter and (abs(delta.iloc[:, 1:].values) > 0.05).any():
            skip = 1

    return concentrations, skip

