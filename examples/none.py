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

    except IndexError:
        pass
    else:
        pass


