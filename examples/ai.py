import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier
from rose.common import obstacles, actions
import os


def convert_world_to_numbers(world):
    game_state = []
    for y in range(10):  # Look 10 steps ahead
        for x in range(3):  # 3 lanes
            try:
                obstacle = world.get((x, world.car.y - y))
                if obstacle == obstacles.NONE:
                    game_state.append(0)
                elif obstacle == obstacles.TRASH:
                    game_state.append(1)
                elif obstacle == obstacles.PENGUIN:
                    game_state.append(2)
                elif obstacle == obstacles.CRACK:
                    game_state.append(3)
                elif obstacle == obstacles.WATER:
                    game_state.append(4)
                else:
                    game_state.append(5)  # Any other obstacle
            except IndexError:
                game_state.append(0)  # Assume empty if out of bounds
    return game_state


def enhance_features(game_states):
    if isinstance(game_states, pd.DataFrame):
        df = game_states
    else:
        df = pd.DataFrame([game_states], columns=[f'lane_{i + 1}_pos_{j + 1}' for i in range(3) for j in range(10)])

    for i in range(3):
        df[f'obstacles_lane_{i + 1}'] = (df.iloc[:, i * 10:(i + 1) * 10] > 0).sum(axis=1)
        df[f'penguins_lane_{i + 1}'] = (df.iloc[:, i * 10:(i + 1) * 10] == 2).sum(axis=1)
        df[f'cracks_lane_{i + 1}'] = (df.iloc[:, i * 10:(i + 1) * 10] == 3).sum(axis=1)

    df['total_obstacles'] = df['obstacles_lane_1'] + df['obstacles_lane_2'] + df['obstacles_lane_3']
    df['total_penguins'] = df['penguins_lane_1'] + df['penguins_lane_2'] + df['penguins_lane_3']
    df['total_cracks'] = df['cracks_lane_1'] + df['cracks_lane_2'] + df['cracks_lane_3']

    # Add more sophisticated features
    df['nearest_penguin'] = df.apply(lambda row: next((i for i, val in enumerate(row[:30]) if val == 2), 30), axis=1)
    df['nearest_crack'] = df.apply(lambda row: next((i for i, val in enumerate(row[:30]) if val == 3), 30), axis=1)
    df['nearest_obstacle'] = df.apply(lambda row: next((i for i, val in enumerate(row[:30]) if val in [1, 4, 5]), 30),
                                      axis=1)

    return df


def generate_reward(moves, game_state):
    reward = 0
    car_position = 1  # Start in the middle lane
    for i, move in enumerate(moves):
        current_state = game_state[i * 3:(i + 1) * 3]
        if move == 2 and current_state[car_position] == 2:  # Picked up penguin
            reward += 10
        elif move == 3 and current_state[car_position] == 3:  # Jumped over crack
            reward += 5
        elif current_state[car_position] in [1, 4, 5]:  # Hit obstacle
            reward -= 10
        elif move in [0, 1]:  # Moved left or right
            reward += 1  # Small reward for movement

        # Update car position
        if move == 0 and car_position > 0:
            car_position -= 1
        elif move == 1 and car_position < 2:
            car_position += 1

    return reward


def train_and_save_model():
    print("Training new model...")

    def generate_random_game_state():
        return np.random.choice([0, 1, 2, 3, 4, 5], size=30, p=[0.7, 0.05, 0.05, 0.05, 0.05, 0.1])

    def generate_smart_moves(game_state):
        moves = []
        car_position = 1  # Start in the middle lane
        for i in range(9):
            current_state = game_state[i * 3:(i + 1) * 3]
            if current_state[car_position] == 2:  # Penguin
                moves.append(2)  # Pickup
            elif current_state[car_position] == 3:  # Crack
                moves.append(3)  # Jump
            elif current_state[car_position] in [1, 4, 5]:  # Obstacle
                if car_position > 0 and current_state[car_position - 1] == 0:
                    moves.append(0)  # Move left
                    car_position -= 1
                elif car_position < 2 and current_state[car_position + 1] == 0:
                    moves.append(1)  # Move right
                    car_position += 1
                else:
                    moves.append(4)  # No action (stay in place)
            else:
                # Look ahead for penguins
                future_state = game_state[(i + 1) * 3:]
                if 2 in future_state:
                    penguin_index = np.where(future_state == 2)[0][0]
                    if penguin_index % 3 != car_position:
                        moves.append(0 if penguin_index % 3 < car_position else 1)
                    else:
                        moves.append(4)  # No action (stay in place)
                else:
                    moves.append(4)  # No action (stay in place)
        return moves

    def train_and_save_model():
        print("Training new model...")

        def generate_random_game_state():
            return np.random.choice([0, 1, 2, 3, 4, 5], size=30, p=[0.7, 0.05, 0.05, 0.05, 0.05, 0.1])

        def create_dataset(n_samples=50000):
            data = []
            for _ in range(n_samples):
                game_state = generate_random_game_state()
                moves = generate_smart_moves(game_state)
                reward = generate_reward(moves, game_state)
                data.append(np.concatenate([game_state, moves, [reward]]))

            columns = [f'lane_{i + 1}_pos_{j + 1}' for i in range(3) for j in range(10)] + \
                      [f'move_{i + 1}' for i in range(9)] + ['reward']

            return pd.DataFrame(data, columns=columns)

        # Create the dataset
        df = create_dataset(n_samples=50000)

        # Enhance features
        X = enhance_features(df.iloc[:, :30])
        y = df.iloc[:, 30:-1]  # Exclude the reward column

        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        # Define and train the XGBoost model
        base_model = XGBClassifier(n_estimators=200, max_depth=10, learning_rate=0.1, n_jobs=-1, random_state=42)
        model = MultiOutputClassifier(base_model)
        model.fit(X_train_scaled, y_train)

        # Save the model and scaler
        joblib.dump(model, 'xgboost_car_game_model.joblib')
        joblib.dump(scaler, 'scaler.joblib')
        print("Model trained and saved successfully.")


def predict_moves(world):
    # Check if model exists, if not, train it
    if not os.path.exists('xgboost_car_game_model.joblib') or not os.path.exists('scaler.joblib'):
        train_and_save_model()

    # Convert world to numbers
    game_state = convert_world_to_numbers(world)

    # Enhance features
    X = enhance_features(game_state)

    # Load the pre-trained model and scaler
    model = joblib.load('xgboost_car_game_model.joblib')
    scaler = joblib.load('scaler.joblib')

    # Scale features
    X_scaled = scaler.transform(X)

    # Make prediction
    prediction = model.predict(X_scaled)

    # Convert prediction to game actions
    action_map = {0: actions.LEFT, 1: actions.RIGHT, 2: actions.PICKUP, 3: actions.JUMP, 4: actions.NONE}
    predicted_actions = [action_map[move] for move in prediction[0]]

    return predicted_actions


def get_next_move(world):
    predicted_moves = predict_moves(world)
    return predicted_moves[0]  # Return the first predicted move