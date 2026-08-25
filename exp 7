import matplotlib.pyplot as plt
import numpy as np

def is_safe(board, row, col):
    """Check if it's safe to place a queen at board[row] = col."""
    for prev_row in range(row):
        placed_col = board[prev_row]
        
        # Check if they are in the same column
        if placed_col == col:
            return False
            
        # Check if they are on the same diagonal
        if abs(prev_row - row) == abs(placed_col - col):
            return False
            
    return True

def solve_n_queens(n):
    """Solve the N-Queens problem using backtracking."""
    board = [-1] * n
    solutions = []
    backtrack_count = [0]
    
    def backtrack(row):
        # If we have successfully placed all n queens
        if row == n:
            solutions.append(board.copy())
            return
            
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col           # Place the queen
                backtrack(row + 1)         # Recurse for the next row
                board[row] = -1            # Undo the placement (backtrack)
            else:
                backtrack_count[0] += 1    # Increment backtrack counter
                
    backtrack(0)
    return solutions, backtrack_count[0]

def print_board(board, n):
    """Print the board to the console."""
    for row in range(n):
        row_string = ""
        for col in range(n):
            if board[row] == col:
                row_string += "Q "
            else:
                row_string += ". "
        print(row_string)
    print()

def plot_board(board_solution, n, solution_idx=1):
    """Visualize the board using matplotlib."""
    # Create an alternating checkerboard pattern
    chessboard = np.zeros((n, n))
    chessboard[1::2, ::2] = 1
    chessboard[::2, 1::2] = 1
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Draw the board (gray and white squares)
    ax.imshow(chessboard, cmap='gray_r', origin='upper', extent=[0, n, n, 0])
    
    # Place the queens on the board
    for row in range(n):
        col = board_solution[row]
        # X is col + 0.5, Y is n - row - 0.5 (to center the text and flip Y-axis correctly)
        ax.text(col + 0.5, row + 0.5, '♕', fontsize=24, 
                ha='center', va='center', color='red', fontweight='bold')
        
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='black', linestyle='-', linewidth=2)
    plt.title(f"{n}-Queens Problem - Solution {solution_idx}")
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    # Test for N = 4, 6, 8
    for n in [4, 6, 8]:
        solutions, backtracks = solve_n_queens(n)
        print(f"--- N = {n} ---")
        print(f"Total Solutions: {len(solutions)}")
        print(f"Total Backtracks: {backtracks}\n")
        
        # Print and plot only the first solution if available to avoid overwhelming output
        if solutions:
            print(f"First solution for N={n} (Console Output):")
            print_board(solutions[0], n)
            
            # Plot the first solution using matplotlib
            print(f"Opening matplotlib window for N={n}...")
            plot_board(solutions[0], n, solution_idx=1)
