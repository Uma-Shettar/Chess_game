import numpy as np
import torch

from RL import encode_board, ChessNet
from controllers import State

# Checks board encoding dimensions, pieces, turn, and castling planes.
def test_encode_board():
    state = State()
    encoded = encode_board(state)

    assert encoded.shape == (18, 8, 8), "Encoded board should have shape (18, 8, 8)"

    assert encoded.dtype == np.float32, "Encoded board should have dtype float32"

    #white pawns
    assert encoded[0].sum() == 8, "There should be 8 white pawns on the board"

    #black pawns
    assert encoded[6].sum() == 8, "There should be 8 black pawns on the board"

    #white king at e1
    assert encoded[5][7][4] == 1, "White king should be at e1"

    #black king at e8
    assert encoded[11][0][4] == 1, "Black king should be at e8"

    #white to move
    assert encoded[12].sum() == 64, "Turn indicator should be set for white to move"

    #castling rights
    for plane in range(13, 17):
        assert encoded[plane].sum() == 64, f"Castling rights plane {plane} should be set to 1 for all squares"

    print("Encode Board Tests Passed!")


# Checks the neural network's output shapes and value range.
def test_network():
    model = ChessNet()

    x = torch.randn(4, 18, 8, 8) 

    policy, value = model(x)

    assert policy.shape == (4,4672), "Policy output should have shape (batch_size, 4672)"

    assert value.shape == (4,1), "Value output should have shape (batch_size, 1)"

    assert torch.all(value >= -1) and torch.all(value <= 1), "Value output should be in the range [-1, 1]"

    print("Network Tests Passed!")



if __name__ == "__main__":
    test_encode_board()
    test_network()

