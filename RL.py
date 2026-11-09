import numpy as np
import torch
import torch.nn as nn

from controllers import Move

PIECE_TO_PLANE = {
    "WP": 0,
    "WN": 1,
    "WB": 2,
    "WR": 3,
    "WQ": 4,
    "WK": 5,
    "BP": 6,
    "BN": 7,
    "BB": 8,
    "BR": 9,
    "BQ": 10,
    "BK": 11
}

# Encodes a game state as neural-network input planes.
def encode_board(s):
    encoded_board = np.zeros((18, 8, 8), dtype=np.float32)
    for r in range(8):
        for c in range(8):
            piece = s.board[r][c]
            if piece != "--":
                plane = PIECE_TO_PLANE[piece]
                encoded_board[plane][r][c] = 1

    #Turn indicator
    if s.white_turn:
        encoded_board[12,:,:] = 1
    
    #Castling rights
    rights = s.castling_rights

    if rights.w_oo:
        encoded_board[13,:,:] = 1
    
    if rights.w_ooo:
        encoded_board[14,:,:] = 1

    if rights.b_oo:
        encoded_board[15,:,:] = 1

    if rights.b_ooo:
        encoded_board[16,:,:] = 1

    
    return encoded_board

# Converts a chess move into its policy-vector index.
def move_to_index(move):

    start = move.from_row * 8 + move.from_column
    end = move.to_row * 8 + move.to_column

    return start * 64 + end

# Converts a policy-vector index back into a board move.
def index_to_move(index, board):
    start = index // 64
    end = index % 64

    from_pos = (start // 8, start % 8)
    to_pos = (end // 8, end % 8)

    return Move(from_pos, to_pos, board)


# Defines a convolutional residual block for the network.
class ResidualBlock(nn.Module):
    # Initializes the convolutional layers and activations.
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU()

    # Applies the residual block to a batch of board features.
    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))

        out += residual

        return self.relu(out)

# Defines the policy/value neural network used by the chess AI.
class ChessNet(nn.Module):
    # Initializes the shared trunk and policy/value heads.
    def __init__(
        self, 
        input_channels=18, 
        channels=64, 
        num_residual_blocks=4, 
        action_size=4096):

        super().__init__()

        # Initial convolutional layer
        self.conv = nn.Conv2d(input_channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU()

        # Residual tower
        self.residual_blocks = nn.Sequential(
            *[
                ResidualBlock(channels) 
                for _ in range(num_residual_blocks)
            ]
        )

        # Policy head
        self.policy_conv = nn.Conv2d(channels, 2, kernel_size=1)

        self.policy_bn = nn.BatchNorm2d(2)
        self.policy_fc = nn.Linear(2 * 8 * 8, action_size)

        # Value head
        self.value_conv = nn.Conv2d(channels, 1, kernel_size=1)
        self.value_bn = nn.BatchNorm2d(1)
        self.value_fc1 = nn.Linear(1 * 8 * 8, 256)
        self.value_fc2 = nn.Linear(256, 1)

    # Computes policy logits and a position-value estimate.
    def forward(self, x):

        #shared feature extraction
        x = self.relu(self.bn(self.conv(x)))
        x = self.residual_blocks(x)

        # policy head
        p = self.relu(self.policy_bn(self.policy_conv(x)))

        p = p.flatten(start_dim=1)
        policy = self.policy_fc(p)

        # value head
        v = self.relu(self.value_bn(self.value_conv(x)))
        v = v.flatten(start_dim=1)
        v = self.relu(self.value_fc1(v))
        value = torch.tanh(self.value_fc2(v))

        return policy, value
