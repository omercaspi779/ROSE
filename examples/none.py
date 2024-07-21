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
            return actions.LEFT
        return actions.NONE
    except IndexError:
        return actions.NONE
    else:
        pass


