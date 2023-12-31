# -*- coding: utf-8 -*-
"""Calc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DDUJVcSmtoPRY2LE76QuQOUp1gPYCBBd

This code file creates graph for the streets considering each street as a node, their properties as the node attributes, and the calculated weigth(Time*severityProportion) as the attribute of the relationship between the nodes. Further, through calculations from traversal, unnecessary relationships have been discarded, as the logic utilized in Predict.py calculated all possible combinations between streets, which is quite redundant. Once, the required edges are calculated, the updated graph is then converted to csv file and uploaded on Neo4j for traversal calculations. There, the weights being so small, have been scaled by a power of 1e6 inorder to add impact to the calculation.
"""

from google.colab import drive

drive.mount('/content/drive')

!pip install pyvis
!pip install networkx pandas
import pandas as pd
import networkx as nx
from pyvis.network import Network

accidents_df = pd.read_csv("/content/drive/MyDrive/US_Accidents.csv")
distances_df = pd.read_csv("/content/drive/MyDrive/filtered_distances.csv")
accidents_df = accidents_df[accidents_df['City'] == 'San Jose']

# Create a directed graph
G = nx.DiGraph()

# Add nodes from US_Accidents.csv
for _, row in accidents_df.iterrows():
    G.add_node(row['Street'],
               amenity=row['Amenity'],
               newAmenity=row['New Amenity'],
               responseTime=row['Response time'],
               severityProportion=row['SeverityProportion'])

# Add edges from filtered_distances.csv
for _, row in distances_df.iterrows():
    G.add_edge(row['Street1'], row['Street2'],
               distance_km=row['Distance (km)'],
               time_minutes=row['Time (minutes)'],
               weight=row['Weight'])

# Convert node IDs to strings if they aren't already
G = nx.relabel_nodes(G, lambda x: str(x))

# Calculate shortest paths for all pairs of nodes
path_dict = dict(nx.all_pairs_dijkstra_path(G, weight='weight'))

# Reconstruct the graph with only necessary edges
H = nx.DiGraph()
for source, target_paths in path_dict.items():
    for target, path in target_paths.items():
        if len(path) > 1:  # Ensure there are intermediate nodes
            for i in range(len(path)-1):
                if not H.has_edge(path[i], path[i+1]):
                    weight = G[path[i]][path[i+1]]['weight']
                    H.add_edge(path[i], path[i+1], weight=weight)

# Assuming H is the optimized graph after dissolving unnecessary edges

# Calculate the number of nodes and edges in the graph H
num_nodes = H.number_of_nodes()
num_edges = H.number_of_edges()

print("Number of nodes:", num_nodes)
print("Number of edges:", num_edges)

import pandas as pd

# Extract edges and their attributes to a DataFrame
edges_df = pd.DataFrame(list(H.edges(data=True)), columns=['Street1', 'Street2', 'Attributes'])
edges_df['Distance (km)'] = edges_df['Attributes'].apply(lambda x: x['weight'])
edges_df.drop('Attributes', axis=1, inplace=True)

edges_df.to_csv('optimized_graph_edges.csv', index=False)
from google.colab import files
files.download('optimized_graph_edges.csv')