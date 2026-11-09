import numpy as np
import torch
import torch.nn.functional as F

from replay_buffer import ReplayBuffer
from RL import ChessNet
from self_play import play_self_game


# Generates self-play games and trains the network from the replay buffer.
def train():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = ChessNet().to(device)

    model.load_state_dict(
        torch.load(
            "chess_model.pth",
            map_location=device
        )
    )

    print("Loaded trained model!")

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=0.001,
        weight_decay=0.0001
    )

    buffer = ReplayBuffer(capacity=100000)

    iterations = 2000
    games_per_iteration = 20
    batch_size = 128
    simulations = 200

    for iteration in range(iterations):

        # SELF PLAY
        model.eval()

        for game in range(games_per_iteration):

            game_data = play_self_game(
                model,
                simulations=simulations,
                device=device
            )

            buffer.add_game(game_data)

        # TRAINING
        if len(buffer) < batch_size:
            continue

        model.train()

        training_steps = 100

        total_loss = 0

        for step in range(training_steps):

            batch = buffer.sample(batch_size)

            states = np.array([
                item[0] for item in batch
            ])

            policies = np.array([
                item[1] for item in batch
            ])

            values = np.array([
                item[2] for item in batch
            ])

            states = torch.tensor(
                states,
                dtype=torch.float32,
                device=device
            )

            policies = torch.tensor(
                policies,
                dtype=torch.float32,
                device=device
            )

            values = torch.tensor(
                values,
                dtype=torch.float32,
                device=device
            ).view(-1, 1)

            predicted_policy, predicted_value = model(states)

            log_policy = F.log_softmax(
                predicted_policy,
                dim=1
            )

            policy_loss = -(
                policies * log_policy
            ).sum(dim=1).mean()

            value_loss = F.mse_loss(
                predicted_value,
                values
            )

            loss = policy_loss + value_loss

            optimizer.zero_grad()

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                1.0
            )

            optimizer.step()

            total_loss += loss.item()

        average_loss = total_loss / training_steps

        print(
            f"Iteration {iteration + 1}/{iterations} "
            f"| Loss: {average_loss:.4f} "
            f"| Buffer: {len(buffer)}"
        )

        torch.save(
            model.state_dict(),
            "chess_model.pth"
        )


if __name__ == "__main__":
    train()
