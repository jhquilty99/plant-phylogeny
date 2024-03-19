import networkx as nx
import pandas as pd


def find_common_ancestor(data_frame, ordering): 
    # Initialize prior column
    old_col = 'EMPTY'
    # With the first iteration, choose the latest ancestor
    if 'Kingdom' in data_frame.columns:
        for col in ordering:
            # Only look for descendants in existing columns
            if col in data_frame.columns:
                # Look for the first column with more than one descendant and return prior column and new column
                unique = data_frame[col].unique()
                if len(unique) > 1 and old_col != 'EMPTY': 
                        return old_col, old_value, unique, col
                # Set the prior column and values for the next iteration
                old_col = col
                old_value = unique[0]
    # With subsequent iterations, choose the earliest ancestor
    else: 
        old_col = data_frame.columns[0]
        old_value = data_frame[old_col].unique()[0]
        for col in ordering:
            # Only look for descendants in existing columns
            if col in data_frame.columns:
                # Look for the first column with more than one descendant and return prior column and new column
                unique = data_frame[col].unique()
                if len(unique) > 1: 
                        return old_col, old_value, unique, col
    return None, None, None, None

def get_descendant_data(df, descendant_level, descendant, ordering):
    df_copy = df.copy()
    for col in ordering:
        if col == descendant_level:
            break
        elif col in df.columns:
            df_copy.drop([col], axis = 1, inplace = True)
    df = df_copy
    return(df[df[descendant_level] == descendant])


def add_descendant_edge_recursion(graph, data_frame, ordering):
    common_level, common_ancestor, descendants, descendant_level = find_common_ancestor(data_frame, ordering)
    if common_level is not None:
        for descendant in descendants: 
            graph.add_edge(common_ancestor, descendant)
            descendant_df = get_descendant_data(
                data_frame, 
                descendant_level, 
                descendant, 
                ordering
            )
            add_descendant_edge_recursion(
                graph, 
                descendant_df, 
                ordering
            )
    return(graph)

def get_node_colors(nodes, data_frame, coloring):
    colors = []
    for node in nodes:
        print(node)
        print(data_frame.columns)
        # Check if the value exists in any column
        for col in data_frame.columns:
            
            print(data_frame[col].values)
            if node in data_frame[col].values:
                colors.append(coloring[col])
                print(str(node) + ' ' + str(col))
                break 
    return(colors)

def visualize_genetic_relationships(data_frame, ordering, ax, coloring):
    """
    Visualizes genetic relationships between species as clades using Divisive Hierarchical Clustering.

    Parameters:
    - data_frame: pandas DataFrame with hierarchical levels of different species.

    Returns:
    - None (displays the dendrogram plot).
    """
    graph = nx.DiGraph() 
    G = add_descendant_edge_recursion(graph, data_frame, ordering)
    #print(list(G))
    node_colors = get_node_colors(list(G), data_frame, coloring)
    # Plot the dendrogram
    _, earliest_common_ancestor, _, _ = find_common_ancestor(data_frame, ordering)
    pos = nx.planar_layout(G)
    pos[earliest_common_ancestor] = [0,0]
    pos = nx.spring_layout(
        G, 
        pos = pos, 
        fixed = [earliest_common_ancestor], 
        iterations=200
    )
    nx.draw(
        G, 
        pos, 
        ax = ax, 
        with_labels=True, 
        font_weight='bold', 
        node_size=700, 
        font_size=12
    )
    
    print(node_colors)
    # nx.draw_networkx_nodes(
    #     G, 
    #     pos, 
    #     ax = ax, 
    #     node_size=700, 
    #     node_color=node_colors
    # )