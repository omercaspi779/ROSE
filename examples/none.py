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

        if obstacle == obstacles.PENGUIN:
            return actions.PICKUP
        if world.get((x - 1, y - 2)) == obstacles.PENGUIN:
            return actions.LEFT
        if world.get((x + 1, y - 2)) == obstacles.PENGUIN:
            return actions.RIGHT


        if obstacle == obstacles.CRACK:
            return actions.JUMP


        if world.get((x-1, y - 2)) == obstacles.CRACK:
            if world.get((x-1, y - 1)) == obstacles.NONE or world.get((x-1, y - 1)) == obstacles.CRACK or world.get((x-1, y - 1)) == obstacles.WATER or world.get((x-1, y - 1)) == obstacles.PENGUIN:
                return actions.LEFT
            else:
                return actions.NONE
        if world.get((x + 1, y - 2)) == obstacles.CRACK:
            if world.get((x+1, y - 1)) == obstacles.NONE or world.get((x+1, y - 1)) == obstacles.CRACK or world.get((x+1, y - 1)) == obstacles.WATER or world.get((x+1, y - 1)) == obstacles.PENGUIN:
                return actions.RIGHT
            else:
                return actions.NONE

        if obstacle == obstacles.WATER:
            return actions.BRAKE
        if world.get((x-1, y - 2)) == obstacles.WATER:
            if world.get((x-1, y - 1)) == obstacles.NONE or world.get((x-1, y - 1)) == obstacles.CRACK or world.get((x-1, y - 1)) == obstacles.WATER or world.get((x-1, y - 1)) == obstacles.PENGUIN:
                return actions.LEFT
            else:
                return actions.NONE
        if world.get((x + 1, y - 2)) == obstacles.WATER:
            if world.get((x+1, y - 1)) == obstacles.NONE or world.get((x+1, y - 1)) == obstacles.CRACK or world.get((x+1, y - 1)) == obstacles.WATER or world.get((x+1, y - 1)) == obstacles.PENGUIN:
                return actions.RIGHT
            else:
                return actions.NONE



        if obstacle == obstacles.NONE:
            return actions.NONE



        if obstacle != obstacles.NONE and obstacle != obstacles.PENGUIN and obstacle != obstacles.WATER and obstacle != obstacles.CRACK: #obstacle infront me
            safe_steps_left = 0
            left_penguines=0
            counter_left=0

            safe_steps_right = 0
            right_penguines=0
            counter_right=0

            end_left = True
            end_right = True

            while end_left:
                if world.get((x-1, y-counter_left)) == obstacles.NONE or world.get((x-1, y-counter_left)) == obstacles.PENGUIN or world.get((x-1, y-counter_left)) == obstacles.WATER or world.get((x-1, y-counter_left)) == obstacles.CRACK: #left
                    safe_steps_left+=1
                if world.get((x-1, y-counter_left)) == obstacles.PENGUIN:
                    left_penguines+=1
                else:
                    end_left=False
                if safe_steps_left == 7:
                    end_left = False
                counter_left+=1

            while end_right:
                if world.get((x+1, y-counter_right)) == obstacles.NONE or world.get((x+1, y-counter_right)) == obstacles.PENGUIN or world.get((x+1, y-counter_left)) == obstacles.WATER or world.get((x+1, y-counter_left)) == obstacles.CRACK: #right
                    safe_steps_right+=1
                if world.get((x+1, y-counter_right)) == obstacles.PENGUIN:
                    right_penguines+=1
                else:
                    end_right=False
                if safe_steps_right == 7:
                    end_right = False
                counter_right+=1

            if safe_steps_left > safe_steps_right: #prefer the left
                return actions.LEFT
            elif safe_steps_right > safe_steps_left: #prefer the right
                return actions.RIGHT
            else: #equels, check for penguins
                if right_penguines > left_penguines: #PREFER THE RIGHT BECAUSE PENGUINS
                    return actions.RIGHT
                elif right_penguines < left_penguines: #PREFER THE LEFT BECAUSE PENGUINS
                    return actions.LEFT
                else:
                    return actions.RIGHT
        return actions.NONE


    except IndexError:
        if x == 5:
            if obstacle != obstacles.NONE and obstacle != obstacles.PENGUIN and obstacle!= obstacles.WATER and obstacle != obstacles.CRACK:
                return actions.LEFT
            elif obstacle == obstacles.PENGUIN:
                return actions.PICKUP
            elif obstacle == obstacles.CRACK:
                return actions.JUMP
            elif obstacle == obstacles.WATER:
                return actions.BRAKE

            if world.get((x - 1, y - 2)) == obstacles.PENGUIN:
                return actions.LEFT

            if world.get((x - 1, y - 2)) == obstacles.CRACK:
                if world.get((x - 1, y - 1)) == obstacles.NONE or world.get(
                        (x - 1, y - 1)) == obstacles.CRACK or world.get((x - 1, y - 1)) == obstacles.WATER or world.get(
                        (x - 1, y - 1)) == obstacles.PENGUIN:
                    return actions.LEFT
                else:
                    return actions.NONE

            if world.get((x - 1, y - 2)) == obstacles.WATER:
                if world.get((x - 1, y - 1)) == obstacles.NONE or world.get((x - 1, y - 1)) == obstacles.CRACK or world.get((x - 1, y - 1)) == obstacles.WATER or world.get((x - 1, y - 1)) == obstacles.PENGUIN:
                    return actions.LEFT
                else:
                    return actions.NONE


        elif x == 0:
            if obstacle != obstacles.NONE and obstacle != obstacles.PENGUIN and obstacle!= obstacles.WATER and obstacle != obstacles.CRACK:
                return actions.RIGHT
            elif obstacle == obstacles.PENGUIN:
                return actions.PICKUP
            elif obstacle == obstacles.CRACK:
                return actions.JUMP
            elif obstacle == obstacles.WATER:
                return actions.BRAKE

            elif world.get((x + 1, y - 2)) == obstacles.PENGUIN:
                return actions.RIGHT

            if world.get((x + 1, y - 2)) == obstacles.CRACK:
                if world.get((x + 1, y - 1)) == obstacles.NONE or world.get(
                        (x + 1, y - 1)) == obstacles.CRACK or world.get((x + 1, y - 1)) == obstacles.WATER or world.get(
                        (x + 1, y - 1)) == obstacles.PENGUIN:
                    return actions.RIGHT
                else:
                    return actions.NONE

            if world.get((x + 1, y - 2)) == obstacles.WATER:
                if world.get((x + 1, y - 1)) == obstacles.NONE or world.get(
                        (x + 1, y - 1)) == obstacles.CRACK or world.get((x + 1, y - 1)) == obstacles.WATER or world.get(
                        (x + 1, y - 1)) == obstacles.PENGUIN:
                    return actions.RIGHT
                else:
                    return actions.NONE

        return actions.NONE
    else:
        pass


