import networkx as nx


def build_graph(df):
    graph = nx.DiGraph()

    graph.add_nodes_from(df['id'])

    def parse_blockers(blockers_column):
        if not isinstance(ticket[1], str) or not ticket[1]:
            return []

        return [blocker for blocker in blockers_column.strip().split(',')]

    for ticket in df[['id', 'is_blocked_by']].values:
        ticket_id = ticket[0]
        ticket_blockers = parse_blockers(ticket[1])

        for blocker in ticket_blockers:
            graph.add_edge(blocker, ticket_id)

    return graph