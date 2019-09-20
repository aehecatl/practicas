# -*- coding: utf-8 -*-
#agrego una klinea aqui
'''
The self-optimization is mainly explored in the following works:

[1] Watson, R. A., Buckley, C. L., & Mills, R. (2009). The effect of hebbian learning on optimization in hopfield networks.
    Technical Report, ECS, University of Southampton

[2] Watson, R. A., Buckley, C. L., & Mills, R. (2011).
    Optimization in “self-modeling” complex adaptive systems. Complexity, 16(5), 17-26. doi:10.1002/cplx.20346

[3] Watson, R. A., Buckley, C. L., & Mills, R. (2011). Global Adaptation in Networks of Selfish Components: Emergent Associative Memory at the System Scale.
    Artificial Life, 17(3), 147-166. doi:10.1162/artl_a_00029

[4] Watson, R. A., Mills, R., & Buckley, C. L. (2011). Transformations in the scale of behavior and the global optimization of constraints in adaptive networks.
    Adaptive Behavior, 19(4), 227-249. doi:10.1177/1059712311412797----------------------------------->>>>>>>>>>>>>>>>>>>><

[5] Watson, R. A., Buckley, C. L., Mills, R., & Davies, A. (2010). Associative memory in gene regulation networks.
    Twelfth International Conference on the Synthesis and Simulation of Living Systems (Artificial Life XII), Odense, Denmark.

[6] Zarco, M., & Froese, T. (2018). Self-modeling in Hopfield Neural Networks with Continuous Activation Function.
    Procedia Computer Science, 123, 573-578. doi:10.1016/j.procs.2018.01.087


[3] Watson, R. A., Buckley, C. L., & Mills, R. (2011). Global Adaptation in Networks of Selfish Components: Emergent Associative Memory at the System Scale.
    Artificial Life, 17(3), 147-166. doi:10.1162/artl_a_00029

[4] Watson, R. A., Mills, R., & Buckley, C. L. (2011). Transformations in the scale of behavior and the global optimization of constraints in adaptive networks.
    Adaptive Behavior, 19(4), 227-249. doi:10.1177/1059712311412797----------------------------------->>>>>>>>>>>>>>>>>>>><

[5] Watson, R. A., Buckley, C. L., Mills, R., & Davies, A. (2010). Associative memory in gene regulation networks.
    Twelfth International Conference on the Synthesis and Simulation of Living Systems (Artificial Life XII), Odense, Denmark.

[6] Zarco, M., & Froese, T. (2018). Self-modeling in Hopfield Neural Networks with Continuous Activation Function.
    Procedia Computer Science, 123, 573-578. doi:10.1016/j.procs.2018.01.087

'''

import networkx as nx
import numpy as np

# HNN stands for discrete-time, discrete-state Hopfield Neural Network
class HNN:

    # the random seed is set
    # all states are set to zero
    def __init__(self, size):
        self.size = size
        #np.random.seed(12348473)
        self.G = nx.Graph()
        self.G.add_nodes_from([x for x in range(self.size)], state=0)

    # Weights are randomized
    # The network is defined with symmetric connections without self-recurrent connections.
    def randomize_weights(self):
        for i in range(0, self.size, 1):
            for j in range(i, self.size, 1):
                # Self-recurrent connections are not allowed in the most basic model
                # However, these connections were set to 1 in [4]
                if i==j:
                    self.G.add_edge(i, j, weight=0, weight_original=0)
                else:
                    w = np.random.uniform(-1, 1)
                    self.G.add_edge(i, j, weight=w, weight_original=w)


    # States are randomized in a discrete way {-1,1}
    # In other works states can be continuous (e.g. [5] and [6])
    def randomize_states(self):
        for i in range(self.size):
            if np.random.uniform(0,1) < 0.5:
                self.G.node[i]['state'] = -1
            else:
                self.G.node[i]['state'] = 1

    # Heaviside funcion used to constrain states in {-1,1} when updated
    def heaviside_function(self, argument):
        if argument < 0:
            return -1
        else:
            return 1

    # Asynchronous update (i.e. states are update one at time)
    def update_states(self):
        ran_node = np.random.randint(self.size)   #np.random.choice(self.size, 1, replace=False)
        #print ran_node
        new_state = 0
        for j in range(self.size):
            new_state = new_state + self.G[ran_node][j]['weight']*self.G.node[j]['state']
        self.G.node[ran_node]['state'] = self.heaviside_function(new_state)

    # Threshold function used to constrain weights in [-1,1]
    def threshold_function(self, argument):
        if argument < -1:
            return -1
        elif argument > 1:
            return 1
        else:
            return argument

    # Hebbian learning rule applied at the end of the relaxation period
    # The learning rate, delta, can be changed to applied learning during relaxation
    def hebbian_learning(self, delta):
        for i in range(self.size):
            for j in range(i, self.size):
                    if i != j:
                        self.G[i][j]['weight'] = self.threshold_function( self.G[i][j]['weight'] +
                                                       delta*self.G.node[i]['state']*self.G.node[j]['state'])

    # The original energy function uses the weights that define the original constraint satisfaction problem.
    # That mean, the original weights are not updated by Hebbian learning.
    def energy_function(self):
        energy = 0
        for i in range(self.size):
            for j in range(self.size):
                energy = energy + self.G[i][j]['weight_original']*self.G.node[i]['state']*self.G.node[j]['state']
        return -energy


    def constraint(self):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                c = self.G[i][j]['weight']*self.G.node[i]['state']*self.G.node[j]['state']
                if c > 0:
                    count = count+1
        return count

    # delta: learning rate
    # tau: steps to reach an atractor
    # relaxations: how many times the network is allowed to reach an attractor
    def self_modeling(self, delta, tau, relaxations):
        print(self.constraint())
        for r in range(relaxations):

            # Reaching an attractor
            for t in range(tau):
                self.update_states()
                # The energy can be checked when the states are been updated
                # The energy always decreased if the connections are symmetric without self-recurrency
                #print(self.energy_function())

            # If the energy is measured here, it does not always decrease
            # The energy at the end of the process should be lower than the energy at the beginning
            print(self.energy_function())

            # Learning is applied to reinforce attractors
            self.hebbian_learning(delta)

            # States are randomized such that the network can explored the state space properly
            self.randomize_states()

        print(self.constraint())


if __name__ == '__main__':

    size = 50
    network = HNN(size)
    network.randomize_states()
    network.randomize_weights()

    network.self_modeling(0.001, 10, 10)
