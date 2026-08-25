import math
import matplotlib.pyplot as plt

# --- 1. First Fit Algorithm ---
def first_fit(items, capacity=1.0):
    bins_space = []       # Remaining space in each bin
    bin_contents = []     # Items stored in each bin
    
    for item in items:
        placed = False
        for i, space in enumerate(bins_space):
            if space >= item:
                bins_space[i] -= item
                bin_contents[i].append(item)
                placed = True
                break
        
        # If item doesn't fit in any existing bin, create a new one
        if not placed:
            bins_space.append(capacity - item)
            bin_contents.append([item])
            
    return bin_contents

# --- 2. First Fit Decreasing Algorithm ---
def first_fit_decreasing(items, capacity=1.0):
    # Sort items in descending order, then apply First Fit
    return first_fit(sorted(items, reverse=True), capacity)

# --- 3. Best Fit Decreasing Algorithm ---
def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)
    bins_space = []
    bin_contents = []
    
    for item in sorted_items:
        best_idx = -1
        best_space = float('inf')
        
        # Find the bin that will have the minimum leftover space after placing the item
        for i, space in enumerate(bins_space):
            if space >= item and (space - item) < best_space:
                best_space = space - item
                best_idx = i
                
        if best_idx != -1:
            bins_space[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            # Create a new bin
            bins_space.append(capacity - item)
            bin_contents.append([item])
            
    return bin_contents

# --- 4. Console Text Display ---
def display_bins(label, bin_contents, capacity=1.0):
    print(f"\n{label}: {len(bin_contents)} bins")
    for i, b in enumerate(bin_contents, 1):
        used = sum(b)
        # Create a text-based progress bar
        bar_fill = int((used / capacity) * 20)
        bar = '█' * bar_fill + '-' * (20 - bar_fill)
        items_str = [round(x, 2) for x in b]
        print(f"  Bin {i}: [{bar}] Used: {used:.2f}/{capacity} | Items: {items_str}")

# --- 5. Matplotlib Visualization ---
def plot_bins(ff_bins, ffd_bins, bfd_bins, capacity=1.0):
    """ Plot stacked bar charts for the 3 algorithms. """
    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=True)
    
    datasets = [
        ("First Fit (FF)", ff_bins),
        ("First Fit Decreasing (FFD)", ffd_bins),
        ("Best Fit Decreasing (BFD)", bfd_bins)
    ]
    
    for ax, (title, bins) in zip(axes, datasets):
        x_pos = range(1, len(bins) + 1)
        
        # Stack items inside each bin
        for bin_idx, b in enumerate(bins):
            bottom = 0
            for item in b:
                # Use a distinct color palette
                ax.bar(bin_idx + 1, item, bottom=bottom, edgecolor='black', width=0.6)
                # Label the item size inside the bar
                ax.text(bin_idx + 1, bottom + item/2, f"{item}", 
                        ha='center', va='center', color='white' if item >= 0.3 else 'black', 
                        fontsize=9, fontweight='bold')
                bottom += item
                
        ax.set_title(f"{title}\nTotal Bins Used: {len(bins)}", fontweight='bold')
        ax.set_xlabel("Bin Number")
        if ax == axes[0]:
            ax.set_ylabel("Capacity Used")
        
        ax.set_xticks(x_pos)
        ax.set_ylim(0, capacity + 0.05)
        ax.axhline(y=capacity, color='red', linestyle='--', label=f"Max Capacity ({capacity})")
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
    plt.tight_layout()
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    # Items sequence restored from the broken scan
    items = [0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5]
    capacity = 1.0
    
    # Calculate Theoretical Lower Bound (Ceiling of total weight / capacity)
    total_weight = sum(items)
    lower_bound = math.ceil(total_weight / capacity)
    
    print("--- Bin Packing Analysis ---")
    print(f"Capacity per bin: {capacity}")
    print(f"Total Sum of Items: {total_weight:.2f}")
    print(f"Theoretical Lower Bound of Bins: {lower_bound}")
    
    # Run the Algorithms
    ff_bins = first_fit(items, capacity)
    ffd_bins = first_fit_decreasing(items, capacity)
    bfd_bins = best_fit_decreasing(items, capacity)
    
    # Console Output
    display_bins('First Fit (FF)', ff_bins, capacity)
    display_bins('First Fit Decreasing (FFD)', ffd_bins, capacity)
    display_bins('Best Fit Decreasing (BFD)', bfd_bins, capacity)
    
    print(f"\n--- Summary ---")
    print(f"Lower Bound: {lower_bound} bins")
    print(f"FF Bins:  {len(ff_bins)}")
    print(f"FFD Bins: {len(ffd_bins)}")
    print(f"BFD Bins: {len(bfd_bins)}")
    
    # Display the Graph
    print("\nOpening matplotlib visualization...")
    plot_bins(ff_bins, ffd_bins, bfd_bins, capacity)
