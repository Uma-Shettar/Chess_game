import copy

import numpy as np

from mcts import get_action_probabilities, run_mcts
from RL import encode_board, move_to_index


# Plays one MCTS self-play game and returns training examples.
def play_self_game(model, simulations = 100, device = 'cpu', temperature_moves = 20):
    from controllers import State, Move

    state = State()
    game_history = []
    move_number = 0

    while True:
        if state.checkmate:
            result = -1 if state.white_turn else 1
            break

        if state.draw:
            result = 0
            break

        root = run_mcts(state, model, simulations, device)

        temperature = 1 if move_number < temperature_moves else 0

        policy, actions = get_action_probabilities(root, temperature)

        if not actions:
            if state.checkmate:
                result = -1.0 if state.white_turn else 1.0
            else :
                result = 0.0
            break

        policy_target = np.zeros(4096, dtype = np.float32)

        for action, probability in policy.items():
            policy_target[action] = probability
        
         # Record current position
        game_history.append({
            "state": encode_board(state).copy(),
            "policy": policy_target,
            "white_turn": state.white_turn
        })

        # Select move
        actions_array = np.array(actions)

        probabilities = np.array([
            policy[action] for action in actions
        ])

        selected_action = np.random.choice(
            actions_array,
            p=probabilities
        )

        selected_move = root.children[
            selected_action
        ].move

        state.play_move(selected_move)

        move_number += 1

        # Optional maximum game length
        if move_number >= 300:
            result = 0.0
            break

    # Generate training samples
    training_data = []

    for position in game_history:

        # Value from the perspective of the player
        # who was to move in this position.
        value = (
            result if position["white_turn"]
            else -result
        )

        training_data.append((
            position["state"],
            position["policy"],
            value
        ))

    return training_data
