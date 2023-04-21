from PIL import Image
import numpy as np
from numpy import asarray
import variables as v
import draw as d
import random


in_img = Image.open(v.image_path)
num_cols, num_rows = in_img.size
if num_cols > 50 or num_rows > 50:
	x = max(num_cols, num_rows)
	divisor = x // 50
	in_img = in_img.resize((num_cols//divisor, num_rows//divisor))
	num_cols, num_rows = in_img.size

in_arr = asarray(in_img)


if v.image_type == "png":
	color_len = 4 ## rgba
elif v.image_type ==  "jpg":
	color_len = 3 ## rgb

out_arr = np.full((4*num_rows, 4*num_cols, color_len), 255, dtype = np.uint8)


for row in range(num_rows):
	brick_length = 0
	new_gaps = []
	col = 0
	while col < num_cols:
		if v.color_mode == 0:
			color = in_arr[row][col]
		elif brick_length == 0:
			if v.image_type == "png":
				color = random.choice(v.lego_colors_rgba)
			elif v.image_type == "jpg":
				color = random.choice(v.lego_colors_rgb)

		## TODO: preserve color (end brick when color changes)

		if d.not_background(in_arr[row][col]) and brick_length == 0: ## pixel is colored and not currently drawing a brick
			d.start_brick(row, col, out_arr, color)
			brick_length = 1
			if v.color_mode == 0 and col < num_cols  - 1 and not d.same_color(color, in_arr[row][col+1]) and d.not_background(in_arr[row][col+1]):
				d.end_brick(row, col, out_arr, color, brick_length)

		elif d.not_background(in_arr[row][col]) and brick_length: ## pixel is colored and are currently drawing a brick
			if brick_length + 1 == max(v.brick_lengths): ## this is the final addition we can make to the current brick
				if col in previous_gaps: # if gap, can't end here; need to make a shorter brick
					col -= 1
					if v.color_mode == 1:
						d.end_brick(row, col, out_arr, color, brick_length)
					else:
						d.end_brick(row, col, out_arr, in_arr[row][col], brick_length)
					brick_length = 0
				else:
					d.end_brick(row, col, out_arr, color, brick_length)
					brick_length = 0

				if col < num_cols - 1:
					if d.not_background(in_arr[row][col+1]):
						new_gaps.append(col) ## gap is to the right of the stored index

			elif v.color_mode == 0 and col < num_cols - 1 and not d.same_color(color, in_arr[row][col+1]) and d.not_background(in_arr[row][col+1]):
				d.end_brick(row, col, out_arr, color, brick_length+1)
				brick_length = 0
				new_gaps.append(col)

			else: ## can keep extending brick
				d.continue_brick(row, col, out_arr, color)
				brick_length += 1

		elif brick_length: ## pixel is not colored and are currently drawing a brick
			if v.color_mode == 1:
				d.end_brick(row, col-1, out_arr, color, brick_length)
			elif v.color_mode == 0:
				d.end_brick(row, col-1, out_arr, in_arr[row][col-1], brick_length) # should make sure length + 1 is a possible length, use color of last pixel in brick
			brick_length = 0

		if brick_length and col == num_cols - 1:  ## drawing a brick and reach the rightmost column of the image
			d.end_brick(row, col, out_arr, color, brick_length)
		col += 1
	previous_gaps = new_gaps


for col in range(num_cols):
	brick = False
	for row in range(1, num_rows):
		if d.not_background(in_arr[row][col]):
			if brick == False:
				if v.color_mode == 1:
					d.draw_stud(row - 1, col, out_arr, out_arr[row*4][col*4])
				elif v.color_mode == 0:
					d.draw_stud(row - 1, col, out_arr)
				if not v.studs_on_all_bricks:
					brick = True
		else:
			brick = False


out_img = Image.fromarray(out_arr)
out_img.save(f"lego-{v.image_path}")