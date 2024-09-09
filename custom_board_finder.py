import pickle
from collections import Counter
import numpy as np


NUMBER_OF_BOARDS = 300


boards = []
board_counters = []
for seed in range(NUMBER_OF_BOARDS):
    with open(f'debugging_boards/pickle_{seed}.pkl', 'rb') as f:
        board = pickle.load(f)
        boards.append(board)
        board_counter = Counter(cell for row in board for cell in row)
        board_counters.append(np.array([board_counter[tile] for tile in range(1, 6)]))


def distance_between_boards(b1, b2):
    return sum(abs(b1 - b2))


distance_matrix = np.zeros((NUMBER_OF_BOARDS, NUMBER_OF_BOARDS))
for i, b1 in enumerate(board_counters):
    for j, b2 in enumerate(board_counters):
        distance_matrix[i, j] = distance_between_boards(b1, b2)


def find_maximal_set(adj_matrix, prefered_node_index, max_distance):
    # Initialize an empty set to hold the maximal set of nodes
    maximal_set = [prefered_node_index]

    # Get the number of nodes
    num_nodes = adj_matrix.shape[0]

    # Iterate through each node
    for node in range(num_nodes):
        if node == prefered_node_index:
            continue

        # Assume the node can be added to the maximal set
        can_add = True

        # Check if this node is compatible with the current set
        for selected_node in maximal_set:
            if adj_matrix[node, selected_node] >= max_distance:
                can_add = False
                break
        
        # If compatible, add the node to the maximal set
        if can_add:
            maximal_set.append(node)

    return maximal_set



# Find the maximal set of nodes
for pref_node in range(NUMBER_OF_BOARDS):
    maximal_nodes = find_maximal_set(distance_matrix, prefered_node_index=pref_node, max_distance=6)
    if len(maximal_nodes) > 8:
        print(f"Number of nodes in the maximal set for {pref_node}: {len(maximal_nodes)} -- {maximal_nodes}")
