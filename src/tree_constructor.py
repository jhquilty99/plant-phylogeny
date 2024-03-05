import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def find_common_ancestor(data_frame, ordering): 
    old_col = 'EMPTY'
    for col in ordering:
        unique = data_frame[col].unique()
        if len(unique) > 1:
            if old_col != 'EMPTY': 
                return old_col, old_value, unique, col
            else:
                return None, None, None, None
        old_col = col
        old_value = data_frame[col].unique()[0]


def add_descendant_edge_recursion(graph, data_frame, ordering):
    common_level, common_ancestor, descendants, descendant_level = find_common_ancestor(data_frame, ordering)
    if common_level is not None:
        for descendant in descendants: 
            graph.add_edge(common_ancestor, descendant)
            descendant_df = data_frame[data_frame[descendant_level] == descendant]
            add_descendant_edge_recursion(graph, descendant_df, ordering)
    return(graph)