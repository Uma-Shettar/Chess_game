import random
from collections import deque


# Stores and samples training positions from self-play games.
class ReplayBuffer:

    # Creates a replay buffer with a fixed maximum capacity.
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)

    # Adds all positions from a completed game to the buffer.
    def add_game(self, game_data):
        self.buffer.extend(game_data)

    # Returns a random batch of stored training positions.
    def sample(self, batch_size):

        return random.sample(
            self.buffer,
            min(batch_size, len(self.buffer))
        )

    # Returns the number of positions currently stored.
    def __len__(self):
        return len(self.buffer)
