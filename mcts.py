import copy
import random

import numpy as np
import torch

from RL import *


# Represents one position in the Monte Carlo search tree.
class Node:
    # Initializes a node's prior, move, statistics, and children.
    def __init__(self, prior=0, move=None):

        self.prior = float(prior)
        self.move = move
        self.visit_count = 0
        self.value_sum = 0

        self.children = {}
        self.expanded = False

    # Returns the node's mean backed-up value.
    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

# Selects the child with the highest PUCT exploration score.
def select_child(node, c_puct=1.5):
    best_score = -float('inf')
    best_action = None
    best_child = None

    for action, child in node.children.items():

        q_value = -child.value()
        u_value = c_puct * child.prior * np.sqrt(node.visit_count) / (1 + child.visit_count)
        score = q_value + u_value

        if score > best_score:
            best_score = score
            best_action = action
            best_child = child

    return best_action, best_child

# Returns the value of a finished game, or None if it is ongoing.
def terminal_value(state):
    if state.checkmate:
        if state.white_turn:
            return -1  # Black wins
        else:
            return 1   # White wins
    if state.draw:
        return 0  # Draw

    return None  # Game is not over


# Evaluates a position and returns policy logits and value.
def evaluate_network(model, state, device):
    board = encode_board(state)
    board_tensor = torch.tensor(board, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        policy_logits, value = model(board_tensor)
        policy_logits = policy_logits.squeeze(0)
        value = value.item()

    return policy_logits.cpu().numpy(), value

# Adds legal-move children to a node using network policy priors.
def expand_node(node, state, model, device):

    legal_moves = state.get_valid_moves()

    random.shuffle(legal_moves)

    if len(legal_moves) == 0:
        return terminal_value(state)

    policy_logits, value = evaluate_network(model, state, device)

    legal_actions = []
    legal_logits = []

    for move in legal_moves:
        action = move_to_index(move)
        if action in legal_actions:
            raise ValueError(f"Duplicate action found: {action}")

        legal_actions.append(action)
        legal_logits.append(policy_logits[action])

    legal_logits = np.array(legal_logits, dtype=np.float64)

    legal_logits -= np.max(legal_logits)
    probabilities = np.exp(legal_logits)
    probabilities /= np.sum(probabilities)

    for move, action, prob in zip(legal_moves, legal_actions, probabilities):
        node.children[action] = Node(prior=prob, move=move)

    node.expanded = True
    return value


# Updates visit and value statistics along a completed search path.
def backpropagate(search_path, value):
    for node in reversed(search_path):
        node.value_sum += value
        node.visit_count += 1
        value = -value  # Switch perspective for the opponent

# Runs one MCTS traversal, expansion, and backpropagation.
def run_simulation(root, state, model, device, c_puct=1.5):
    
    current_state = copy.deepcopy(state)
    node = root
    search_path = [node]

    while node.expanded and node.children:
        action, child = select_child(node, c_puct)
        node = child
        search_path.append(node)

    #evaluation
    value = terminal_value(current_state)

    if value is None:
        value = expand_node(node, current_state, model, device)

    backpropagate(search_path, value)

# Builds a search tree by running the requested number of simulations.
def run_mcts(state, model, simulations = 100, device="cpu", c_puct=1.5):
    model.eval()

    root = Node()

    value = expand_node(root, state, model, device)

    if value is not None:
        return root
    
    for _ in range(simulations):
        run_simulation(root, state, model, device, c_puct)

    return root

# Converts root-child visit counts into move probabilities.
def get_action_probabilities(root, temperature=1.0):
    
    actions = list(root.children.keys())

    visits = np.array([root.children[a].visit_count for a in actions], dtype=np.float64)

    if len(actions) == 0:
        return {},[]

    if temperature == 0:
        probabilities = np.zeros_like(visits)
        probabilities[np.argmax(visits)] = 1.0

    else:
        visits = visits ** (1 / temperature)

        if visits.sum() == 0:
            probabilities = np.ones_like(visits) / len(visits)
        else:
            probabilities = visits / visits.sum()

    return dict(zip(actions, probabilities)), actions


# Chooses a move from the root using visit-count probabilities.
def choose_move(root, temperature=0.0):
    probabilities, actions = get_action_probabilities(root, temperature)

    if len(actions) == 0:
        return None
    
    probs = np.array([probabilities[a] for a in actions])

    selected_action = np.random.choice(actions, p=probs)

    return root.children[selected_action].move


