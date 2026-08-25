import sys
import time
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

# Increase recursion depth for worst-case Quick Sort scenarios
sys.setrecursionlimit(20000)

comparisons = 0

# --- 1. Partition Logic ---
def partition(arr, low, high):
    global comparisons
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap the pivot element to its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# --- 2. Deterministic Quick Sort ---
def deterministic_quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        deterministic_quicksort(arr, low, pi - 1)
        deterministic_quicksort(arr, pi + 1, high)

# --- 3. Randomized Quick Sort ---
def randomized_quicksort(arr, low, high):
    if low < high:
        # Pick a random pivot index and swap it with the last element (high)
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        
        pi = partition(arr, low, high)
        randomized_quicksort(arr, low, pi - 1)
        randomized_quicksort(arr, pi + 1, high)

# --- 4. Test Runner ---
def run_test(sort_fn, arr):
    global comparisons
    comparisons = 0
    a = arr.copy()  # Make a copy so we don't sort the original list
    
    start = time.perf_counter()
    sort_fn(a, 0, len(a) - 1)
    elapsed = (time.perf_counter() - start) * 1000  # Convert to milliseconds
    
    return comparisons, elapsed

# --- 5. Matplotlib Visualization ---
def plot_results(labels, dqs_comps, rqs_comps, dqs_times, rqs_times):
    x = np.arange(len(labels))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Comparisons Bar Chart
    ax1.bar(x - width/2, dqs_comps, width, label='Deterministic QS', color='#FF6B6B', edgecolor='black')
    ax1.bar(x + width/2, rqs_comps, width, label='Randomized QS', color='#4ECDC4', edgecolor='black')
    ax1.set_ylabel('Number of Comparisons (Log Scale)')
    ax1.set_title('Comparisons by Input Type')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_yscale('log') # Use log scale because Deterministic Worst-Case is exponentially larger
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Time Taken Bar Chart
    ax2.bar(x - width/2, dqs_times, width, label='Deterministic QS', color='#FF6B6B', edgecolor='black')
    ax2.bar(x + width/2, rqs_times, width, label='Randomized QS', color='#4ECDC4', edgecolor='black')
    ax2.set_ylabel('Time Taken (ms)')
    ax2.set_title('Execution Time by Input Type')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Using N=2000. Large enough to show differences, small enough to run instantly.
    N = 2000 
    
    test_cases = {
        'Random': [random.randint(1, 100000) for _ in range(N)],
        'Sorted': list(range(N)),
        'Reverse': list(range(N, 0, -1))
    }

    # Make Nearly Sorted (slightly shuffled)
    ns = test_cases['Sorted'].copy()
    for _ in range(N // 20):
        i, j = random.randint(0, N-1), random.randint(0, N-1)
        ns[i], ns[j] = ns[j], ns[i]
    test_cases['Nearly Sorted'] = ns

    # Data collection arrays for plotting
    labels = []
    dqs_c, rqs_c = [], []
    dqs_t, rqs_t = [], []

    print("-" * 85)
    print(f"{'Input Type':<15} | {'DQS Comps':<12} | {'DQS Time(ms)':<15} | {'RQS Comps':<12} | {'RQS Time(ms)':<15}")
    print("-" * 85)

    for case, arr in test_cases.items():
        # Run Deterministic Quick Sort
        d_comps, d_time = run_test(deterministic_quicksort, arr)
        # Run Randomized Quick Sort
        r_comps, r_time = run_test(randomized_quicksort, arr)
        
        labels.append(case)
        dqs_c.append(d_comps); dqs_t.append(d_time)
        rqs_c.append(r_comps); rqs_t.append(r_time)

        print(f"{case:<15} | {d_comps:<12d} | {d_time:<15.2f} | {r_comps:<12d} | {r_time:<15.2f}")
    
    print("-" * 85)
    
    print("\nOpening matplotlib visualization...")
    plot_results(labels, dqs_c, rqs_c, dqs_t, rqs_t)
