import networkx as nx
import random
import numpy as np
import dwave_networkx as dnx
import dimod
from dwave.system import DWaveSampler, LazyFixedEmbeddingComposite
import dwave.inspector
# Create a problem
G = nx.generators.complete_graph(30)
G.add_edges_from([(u, v, {'sign': 2*random.randint(0, 1) - 1}) for u, v in G.edges])
h, J = dnx.algorithms.social.structural_imbalance_ising(G)
bqm = dimod.BQM.from_ising(h, J)
# Sample on a D-Wave system
num_samples = 1000
sampler = LazyFixedEmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm, num_reads=num_samples)        

print(sampleset.info["embedding_context"]["chain_strength"])    

chains = sampleset.info["embedding_context"]["embedding"].values()  
print(max(len(chain) for chain in chains))               
