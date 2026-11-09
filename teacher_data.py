
import random

import numpy as np

from auto_move import Best_move
from controllers import State
from RL import encode_board, move_to_index

ACTION_SIZE = 4096


# Generates board, policy, and value examples using a minimax teacher.
def generate_teacher_dataset(
    num_games=50,
    depth=3,
    max_moves=200
):

    dataset = []

    for game_number in range(num_games):

        state = State()

        # Alternate which side plays Minimax
        teacher_white = game_number % 2 == 0

        move_number = 0

        while move_number < max_moves:

            if state.checkmate or state.draw:
                break

            valid_moves = state.get_valid_moves()

            if not valid_moves:
                break

            # Save current position
            board_state = encode_board(state).copy()

            # Ask Minimax to evaluate the position
            best_move, evaluation = Best_move(
                state,
                valid_moves,
                depth=depth
            )

            if best_move is None:
                break

            # Create expert policy
            policy = np.zeros(
                ACTION_SIZE,
                dtype=np.float32
            )

            move_index = move_to_index(best_move)

            policy[move_index] = 1.0

            # Convert evaluation into [-1, 1]
            value = np.tanh(evaluation / 10.0)

            dataset.append((
                board_state,
                policy,
                np.float32(value)
            ))

            # Teacher plays one side.
            # Random opponent plays the other.
            if state.white_turn == teacher_white:

                selected_move = best_move

            else:

                selected_move = random.choice(
                    valid_moves
                )

            state.play_move(selected_move)

            move_number += 1

        print(
            f"Game {game_number + 1}/{num_games} "
            f"| Dataset: {len(dataset)}"
        )

    return dataset
