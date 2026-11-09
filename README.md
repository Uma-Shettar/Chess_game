# Chess Game

A Python chess game with a Pygame interface, a custom chess rules engine, and a neural-network AI trained with a combination of expert-guided learning and reinforcement learning through MCTS self-play.

## Features

- Interactive 8x8 chessboard with piece images.
- Legal-move generation, check/checkmate and draw detection, castling, and pawn promotion.
- Neural network with policy and value heads.
- MCTS-based move selection.
- Expert-data and self-play training scripts.

## Learning approach

The project combines two training approaches:

- **Expert-guided training:** A depth-limited minimax teacher generates positions and target moves to train the network.
- **Reinforcement learning through self-play:** The network plays games against itself using MCTS. Training uses the MCTS move probabilities as policy targets and each game's final result as the value target.

## Requirements

- Python 3
- Packages listed in `requirements.txt` (Pygame, NumPy, and PyTorch)

Create and activate a virtual environment on Windows, then install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For a CUDA-enabled PyTorch installation, use the install command recommended by the [official PyTorch instructions](https://pytorch.org/get-started/locally/).

## Run the game

From the project directory:

```powershell
python app.py
```

The application loads `chess_model.pth` when it starts. Keep this checkpoint in the project directory. The human plays White and the AI plays Black.

### Controls

- Click a piece, then click its destination square to move.
- Press **U** to undo one move.
- Press **R** to restart the game.
- Close the window to quit.

## Training

### Train from expert-generated positions

```powershell
python expert_train.py
```

This generates positions using a depth-limited minimax teacher, trains the policy/value network, and saves the resulting weights to `chess_model.pth`. Dataset generation and training can take a while.

### Continue training with self-play

```powershell
python train.py
```

This loads `chess_model.pth`, generates self-play games using MCTS, and updates the checkpoint. It requires an existing checkpoint and is configured for a long training run.

## Tests

Run the included board-encoding and network shape checks with:

```powershell
python test.py
```

## Project files

| File | Purpose |
|---|---|
| `app.py` | Pygame interface and game loop |
| `controllers.py` | Board state, moves, and legal-move generation |
| `RL.py` | Board encoding, move indexing, and neural-network model |
| `RL_AI_move.py` | Loads the model and chooses AI moves |
| `mcts.py` | MCTS search and policy generation |
| `auto_move.py` | Minimax search used by the expert-data generator |
| `teacher_data.py` | Generates training positions using the minimax teacher |
| `expert_train.py` | Trains the model on expert-generated positions |
| `self_play.py` | Generates MCTS self-play games |
| `replay_buffer.py` | Stores self-play training examples |
| `train.py` | Trains the model using self-play |
| `chess_model.pth` | Saved model checkpoint used by the game |
| `images/` | Chess piece images used by the interface |
