import torch

from mcts import choose_move, run_mcts
from RL import ChessNet


# Loads the trained network and provides chess move predictions.
class ChessAI:

    # Initializes the model, device, and search configuration.
    def __init__(self, model_path="chess_model.pth",
                 simulations=200):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model = ChessNet().to(self.device)

        self.model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )

        self.model.eval()

        self.simulations = simulations

    # Selects a move for the current state using MCTS.
    def predict(self, state):

        root = run_mcts(
            state,
            self.model,
            simulations=self.simulations,
            device=self.device
        )

        return choose_move(root, temperature=0)