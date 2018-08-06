import networkx as nx
import pandas as pd

def build_graph(df):
    G=nx.DiGraph()

    G.add_nodes_from(df['id'])

    def parse_blockes(blockers_column):
        if not isinstance(ticket[1], str) or not ticket[1]:
            return []
    
        return [blocker for blocker in blockers_column.strip().split(',')]

    for ticket in df[['id', 'is_blocked_by']].values:
        ticket_id = ticket[0]
        ticket_blockers = parse_blockes(ticket[1])
    
        for blocker in ticket_blockers:
            G.add_edge(blocker, ticket_id)
            
    return G