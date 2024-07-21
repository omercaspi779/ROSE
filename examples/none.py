"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "No Driver"

def drive(world):
    x = world.car.x
    y = world.car.y
    try:
        obstacle = world.get((x, y - 1))
        if obstacle == obstacles.NONE:
            return actions.NONE
        elif obstacle == obstacles.PENGUIN:
            return actions.PICKUP
        if obstacle != obstacles.NONE and obstacle != obstacles.PENGUIN:

            if world.get((x - 1, y)) == obstacles.NONE: # left is good
                if world.get((x + 1, y)) == obstacles.NONE: # right is good also
                    for i in range(9):
                        if world.get((x+1, y-i)) == obstacles.PENGUIN:
                            return actions.RIGHT
                return actions.LEFT

            if world.get((x + 1, y)) == obstacles.NONE: # right is good
                if world.get((x - 1, y)) == obstacles.NONE: #left is good also
                    for i in range(9):
                        if world.get((x-1, y-i)) == obstacles.PENGUIN:
                            return actions.LEFT
                return actions.RIGHT

        return actions.NONE

    except IndexError:
        return actions.NONE
    else:
        pass


