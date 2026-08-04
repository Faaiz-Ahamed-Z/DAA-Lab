import sys
import matplotlib.pyplot as plt
import numpy as np

def matrix_chain_order(p):
    """
    Computes the minimum scalar multiplications needed to multiply 
    a sequence of matrices using Dynamic Programming.
    """
    n = len(p) - 1  # Number of matrices
    
    m = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    s = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = sys.maxsize
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def get_optimal_parens_str(s, i, j):
    """
    Returns the optimal parenthesization as a string.
    """
    if i == j:
        return f"A{i}"
    else:
        left = get_optimal_parens_str(s, i, s[i][j])
        right = get_optimal_parens_str(s, s[i][j] + 1, j)
        return f"({left}{right})"

def plot_matrix_chain_cost(m, s, p):
    """
    Plots a heatmap visualization of the Dynamic Programming cost table m[i][j].
    """
    n = len(p) - 1
    
    # Extract submatrix for indices 1..n to a numpy array
    cost_matrix = np.zeros((n, n))
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            cost_matrix[i-1][j-1] = m[i][j]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Mask the upper/lower invalid triangular parts for better visualization
    masked_matrix = np.ma.masked_where(np.triu(cost_matrix) == 0, cost_matrix)
    # Re-enable the diagonal entries
    for i in range(n):
        masked_matrix[i, i] = 0

    cax = ax.imshow(masked_matrix, cmap="YlOrRd", interpolation="nearest")

    # Add colorbar
    cbar = fig.colorbar(cax)
    cbar.set_label("Scalar Multiplications (Cost)", rotation=270, labelpad=15)

    # Set axis tick labels
    labels = [f"A{i}" for i in range(1, n + 1)]
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    
    ax.set_xlabel("To Matrix (j)", fontsize=12)
    ax.set_ylabel("From Matrix (i)", fontsize=12)
    
    # Annotate cell values
    for i in range(n):
        for j in range(n):
            if i <= j:
                val = int(cost_matrix[i][j])
                ax.text(j, i, f"{val}", ha="center", va="center", 
                        color="black" if val < np.max(cost_matrix)/2 else "white", 
                        fontsize=11, fontweight="bold")

    # Add titles and optimal parenthesization summary
    parens_str = get_optimal_parens_str(s, 1, n)
    min_cost = m[1][n]
    
    plt.title(f"Matrix Chain Multiplication DP Table Cost\nOptimal Paren: {parens_str} | Min Cost: {min_cost}", 
              fontsize=13, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    # Example dimensions:
    # A1: 10x30, A2: 30x5, A3: 5x60
    dimensions = [10, 30, 5, 60]
    
    m, s = matrix_chain_order(dimensions)
    num_matrices = len(dimensions) - 1
    
    # Console output
    print("Matrix Dimensions:", dimensions)
    print(f"Minimum scalar multiplications required: {m[1][num_matrices]}")
    print("Optimal Parenthesization:", get_optimal_parens_str(s, 1, num_matrices))
    
    # Graphical output
    plot_matrix_chain_cost(m, s, dimensions)