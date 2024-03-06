import networkx as nx


def find_common_ancestor(data_frame, ordering): 
    old_col = 'EMPTY'
    for col in ordering:
        if col in data_frame.columns:
            unique = data_frame[col].unique()
            if len(unique) > 1:
                if old_col != 'EMPTY': 
                    return old_col, old_value, unique, col
            old_col = col
            old_value = data_frame[col].unique()[0]
    return None, None, None, None


def add_descendant_edge_recursion(graph, data_frame, ordering):
    common_level, common_ancestor, descendants, descendant_level = find_common_ancestor(data_frame, ordering)
    if common_level is not None:
        for descendant in descendants: 
            graph.add_edge(common_ancestor, descendant)
            descendant_df = data_frame[data_frame[descendant_level] == descendant]
            add_descendant_edge_recursion(graph, descendant_df, ordering)
    return(graph)


def visualize_genetic_relationships(data_frame, ordering, ax):
    """
    Visualizes genetic relationships between species as clades using Divisive Hierarchical Clustering.

    Parameters:
    - data_frame: pandas DataFrame with hierarchical levels of different species.

    Returns:
    - None (displays the dendrogram plot).
    """
    
    G = nx.DiGraph() 

    G = add_descendant_edge_recursion(G, data_frame, ordering)
    # Plot the dendrogram
    pos = nx.spring_layout(G)
    #pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", args="")
    #ax.margins(0.5, 0.5)
    nx.draw(G, pos, ax, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=12)