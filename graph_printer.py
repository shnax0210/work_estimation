def find_pos(G, node, position, v_step, h_step, result):
    result.append((node, position))
    
    sub_nodes = [sub_node for sub_node in G.successors(node) if sub_node != node]
    
    if len(sub_nodes) == 0:
        return
    
    def find_new_position(sub_node_index, position, sub_v_step):
        new_position = position.copy()
    
        if sub_node_index == 0:
            new_position[0] = new_position[0] + h_step
        else:
            new_position[1] = new_position[1] - sub_v_step
            
        return new_position
    
    new_position = position
    
    def find_weits_of_branshes(branches):
        def find_branche_size(branch, current_depth):
            branche_size = current_depth
            
            for sub_branch in G.successors(branch):
                branche_size = branche_size + find_branche_size(sub_branch, current_depth + 1)
                
            return branche_size
            
        
        branche_sizes = [find_branche_size(branch, 1) for branch in branches]
        total_size = sum(branche_sizes)
        
        return [branche_size / total_size for branche_size in branche_sizes]
         
    
    weits_of_branshes = find_weits_of_branshes(sub_nodes)
    
    for sub_node_index in range(len(sub_nodes)):
        sub_v_step = v_step * weits_of_branshes[sub_node_index]
        new_position = find_new_position(sub_node_index, new_position, sub_v_step)
        find_pos(G, sub_nodes[sub_node_index], new_position, sub_v_step, h_step, result)

def buid_pos(G):
    pos = []      
    find_pos(G, 'ProjectStart', [1., -1.], 0.1, 5., pos)
    return dict(pos)

def print_graph(G):
    pos = buid_pos(G)
    plt.rcParams['figure.figsize'] = [96, 48]
    nx.draw_networkx(G, with_labels = True, pos=pos, font_size=30)
    #plt.savefig("graph.svg")