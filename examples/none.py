from rose.common import obstacles, actions
from examples import ai # Import the AI module (assuming the AI code is in a file named ai_module.py)

driver_name = "AI Driver"
move_counter = 0
total_moves = 60000


def drive(world):
    global move_counter
    if move_counter >= total_moves:
        return actions.NONE  # Stop after 60 moves

    next_move = ai.get_next_move(world)
    move_counter += 1
    return next_move