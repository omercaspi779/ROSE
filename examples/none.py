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
    except IndexError:
        pass

    return actions.NONE
