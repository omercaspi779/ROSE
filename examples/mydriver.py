from rose.common import obstacles, actions

driver_name = "Arnon"

def drive(w):
	x = w.car.x
	y = w.car.y

	# look 3 lines ahead
	next_x, score = move(w, x, y, 3)
	print("next_x=", next_x, "score=", score)

	# drive left/right
	if next_x < x:
		return actions.LEFT
	if next_x > x:
		return actions.RIGHT

	# drive straight ahead and act according to the obstacle
	obs = get_obs(w, next_x, y-1)

	if obs == obstacles.PENGUIN:
		return actions.PICKUP
	if obs == obstacles.WATER:
		return actions.BRAKE
	if obs == obstacles.CRACK:
		return actions.JUMP

	return actions.NONE


def move(w, x, y, steps):
	if steps == 0:
		return x, 0

	best_score = 0
	best_next_x = x

	# calculate straight ahead score
	obs = get_obs(w, x, y-1)

	if obs == obstacles.NONE:
		best_score = 10
	elif obs == obstacles.PENGUIN:
		best_score = 20
	elif obs == obstacles.WATER:
		best_score = 4
	elif  obs == obstacles.CRACK:
		best_score = 5
	elif obs == obstacles.TRASH or obs == obstacles.BIKE or obs == obstacles.BARRIER:
		best_score = -10

	_, score = move(w, x, y-1, steps-1)
	best_score += score

	x_min = (x // 3) * 3
	x_max = x_min + 2

	# calculate left/right score and the best move
	for x_iter in [x-1, x+1]:
		if x_iter < x_min or x_iter > x_max:
			continue

		x_score = 0
		obs = get_obs(w, x_iter, y-1)

		if obs in [obstacles.NONE, obstacles.PENGUIN]:
			x_score = 10
		elif obs in [obstacles.WATER, obstacles.CRACK, obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
			x_score = -10

		_, score = move(w, x_iter, y-1, steps-1)
		x_score += score

		if x_score > best_score:
			best_score = x_score
			best_next_x = x_iter

	return best_next_x, best_score

def get_obs(w, x, y):
	try:
		obs = w.get((x, y))
	except IndexError:
		return "IndexError"
	else:
		return obs