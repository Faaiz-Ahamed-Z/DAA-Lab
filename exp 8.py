import copy
from itertools import permutations
import networkx as nx
import matplotlib.pyplot as plt

INF = float('inf')

# --- 1. Matrix Reduction (Used for Branch and Bound approach) ---
def reduce_matrix(mat):
    """ Reduce matrix and return the reduced matrix and reduction cost """
    n = len(mat)
    m = copy.deepcopy(mat)
    total_cost = 0

    # Row reduction: subtract min of each row from all elements in that row
    for i in range(n):
        row_min = min(m[i])
        if row_min != INF and row_min > 0:
            total_cost += row_min
            for j in range(n):
                if m[i][j] != INF:
                    m[i][j] -= row_min

    # Column reduction: subtract min of each column from all elements in that col
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))
        if col_min != INF and col_min > 0:
            total_cost += col_min
            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, total_cost

# --- 2. Brute Force TSP ---
def tsp_brute_force(cost_matrix):
    """ Find the optimal TSP path using brute force permutations """
    n = len(cost_matrix)
    # We assume city 0 is the start and end point. 
    # We permute the remaining cities (1 to n-1)
    cities = list(range(1, n)) 
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        # Create full path: 0 -> permuted cities -> 0
        path = [0] + list(perm) + [0]
        current_cost = 0
        
        # Calculate cost of this specific path
        for i in range(n):
            current_cost += cost_matrix[path[i]][path[i+1]]
            
        # Update if we found a better path
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = path

    return best_path, best_cost

# --- 3. Matplotlib & NetworkX Visualization ---
def plot_tsp(cost_matrix, optimal_path):
    """ Draw the cities and highlight the optimal path """
    n = len(cost_matrix)
    G = nx.DiGraph()
    
    # Add nodes (cities)
    for i in range(n):
        G.add_node(i)
        
    # Generate circular layout positions for nodes
    pos = nx.circular_layout(G)
    plt.figure(figsize=(8, 6))
    
    # Draw all possible paths lightly in the background
    for i in range(n):
        for j in range(n):
            if i != j and cost_matrix[i][j] != INF:
                G.add_edge(i, j)
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', arrows=False)
    
    # Extract the edges from the optimal path
    path_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path)-1)]
    
    # Draw the optimal path in red with arrows
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', 
                           width=2, arrows=True, arrowsize=20)
    
    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Label the weights (costs) only for the edges in the optimal path
    edge_labels = {(u, v): cost_matrix[u][v] for u, v in path_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_weight='bold')
    
    plt.title(f"Travelling Salesman Problem (5-City)\nMinimum Cost: {sum(edge_labels.values())}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Reconstructed 5-City Cost Matrix (Distances to self are INF)
    cost = [
        [INF, 10,  8,   9,   7],
        [10,  INF, 10,  5,   6],
        [8,   10,  INF, 8,   9],
        [9,   5,   8,   INF, 6],
        [7,   6,   9,   6,   INF]
    ]
    
    print("--- 5-City TSP Cost Matrix ---")
    for row in cost:
        # Format INF nicely for the console
        print(["INF" if x == INF else f"{x:3}" for x in row])
        
    # 1. Show the initial matrix reduction cost (Step 1 of Branch and Bound)
    reduced_mat, reduction_cost = reduce_matrix(cost)
    print(f"\nMatrix Reduction Cost (Lower Bound): {reduction_cost}")
    
    # 2. Solve using brute force permutations
    best_path, best_cost = tsp_brute_force(cost)
    path_str = " -> ".join(map(str, best_path))
    
    print(f"\n--- TSP Solution ---")
    print(f"Optimal Path: {path_str}")
    print(f"Minimum Cost: {best_cost}")
    
    # 3. Plot the result
    print("\nOpening matplotlib visualization...")
    plot_tsp(cost, best_path)
