"""
This driver implements a circular path along the x-axis on a grid of any width.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Circular -axis Path Driver"

def drive(world):
    x = world.car.x
    y = world.car.y

    try:

        obstacle = world.get((x, y - 1))

        if obstacle == obstacles.PENGUIN:
            return actions.PICKUP
        if world.get(((x-1)%6, y - 2)) == obstacles.PENGUIN:
            return actions.LEFT
        elif world.get(((x+1)%6, y - 2)) == obstacles.PENGUIN:
            return actions.RIGHT

        if obstacle == obstacles.CRACK:
            return actions.JUMP
        if world.get(((x-1)%6, y - 2)) == obstacles.CRACK:
            return actions.LEFT
        elif world.get(((x+1)%6, y - 2)) == obstacles.CRACK:
            return actions.RIGHT

        if obstacle == obstacles.WATER:
            return actions.BRAKE
        if world.get(((x-1)%6, y - 2)) == obstacles.WATER:
            return actions.LEFT
        elif world.get(((x+1)%6, y - 2)) == obstacles.WATER:
            return actions.RIGHT

        if obstacle == obstacles.NONE:
            return actions.NONE

        if obstacle != obstacles.NONE and obstacle != obstacles.PENGUIN and obstacle != obstacles.WATER and obstacle != obstacles.CRACK:
            safe_steps_left = 0
            left_penguines = 0
            counter_left = 0

            safe_steps_right = 0
            right_penguines = 0
            counter_right = 0

            end_left = True
            end_right = True

            while end_left:
                if world.get((x-1, y-counter_left)) in [obstacles.NONE, obstacles.PENGUIN, obstacles.WATER, obstacles.CRACK]:
                    safe_steps_left += 1
                if world.get((x-1, y-counter_left)) == obstacles.PENGUIN:
                    left_penguines += 1
                else:
                    end_left = False
                if safe_steps_left == 7:
                    end_left = False
                counter_left += 1

            while end_right:
                if world.get(((x+1)%6, y-counter_right)) in [obstacles.NONE, obstacles.PENGUIN, obstacles.WATER, obstacles.CRACK]:
                    safe_steps_right += 1
                if world.get(((x+1)%6, y-counter_right)) == obstacles.PENGUIN:
                    right_penguines += 1
                else:
                    end_right = False
                if safe_steps_right == 7:
                    end_right = False
                counter_right += 1

            if safe_steps_left > safe_steps_right:
                return actions.LEFT
            elif safe_steps_right > safe_steps_left:
                return actions.RIGHT
            else:
                if right_penguines > left_penguines:
                    return actions.RIGHT
                elif right_penguines < left_penguines:
                    return actions.LEFT
                else:
                    return actions.RIGHT
        return actions.NONE

    except IndexError:
        # If we get an IndexError, we've reached a border
        # Try to move in the opposite direction
        try:

            if world.get(((x-1)%6, y)) is not None:
                return actions.LEFT
            elif world.get(((x+1)%6, y)) is not None:
                return actions.RIGHT
        except IndexError:
            # If both sides are out of bounds, stay put
            pass

    # If no other action is taken, move forward
    return actions.NONE