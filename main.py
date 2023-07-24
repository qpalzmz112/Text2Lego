from PIL import Image
import numpy as np
from numpy import asarray
import variables as v
import draw as d
import random
import os


in_img = Image.open(v.image_path)
num_cols, num_rows = in_img.size
if num_cols > 50 or num_rows > 50:
	x = max(num_cols, num_rows)
	divisor = x // 50
	in_img = in_img.resize((num_cols//divisor, num_rows//divisor))
	num_cols, num_rows = in_img.size

in_arr = asarray(in_img)

if len(in_arr[0][0]) == 4:
	color_type = "rgba"
elif len(in_arr[0][0]) == 3:
	color_type = "rgb"

d.set_color_length(len(color_type))

out_arr = np.full((4*num_rows, 4*num_cols, len(color_type)), 255, dtype = np.uint8)


bricks = []
previous_gaps = []
for row in range(num_rows):
	current_brick = [0, 0, 0] # start coordinate, length, color
	brick_length = 0
	new_gaps = []
	col = 0
	while col < num_cols:
		if v.color_mode == 0:
			color = in_arr[row][col]
		elif brick_length == 0:
			if color_type == "rgba":
				color = random.choice(v.lego_colors_rgba)
			elif color_type == "rgb":
				color = random.choice(v.lego_colors_rgb)

		## TODO: preserve color (end brick when color changes)

		if d.not_background(in_arr[row][col]) and brick_length == 0: ## pixel is colored and not currently drawing a brick
			d.start_brick(row, col, out_arr, color)
			brick_length = 1
			current_brick[0] = [row, col]
			current_brick[2] = color
			if v.color_mode == 0 and col < num_cols  - 1 and not d.same_color(color, in_arr[row][col+1]) and d.not_background(in_arr[row][col+1]): # preserving color, color switches
				d.end_brick(row, col, out_arr, color, brick_length)
				current_brick[1] = brick_length
				bricks.append(current_brick)
				current_brick = [0, 0, 0]
				brick_length = 0

		elif d.not_background(in_arr[row][col]) and brick_length: ## pixel is colored and are currently drawing a brick
			if brick_length + 1 == max(v.brick_lengths): ## this is the final addition we can make to the current brick
				if col in previous_gaps: # if there's a gap here, the brick can't end here; need to make a shorter brick
					col -= 1
					if v.color_mode == 1:
						d.end_brick(row, col, out_arr, color, brick_length)
					else:
						d.end_brick(row, col, out_arr, in_arr[row][col], brick_length)
					current_brick[1] = brick_length - 1
					bricks.append(current_brick)
					current_brick = [0, 0, 0]
					brick_length = 0
				else:
					d.end_brick(row, col, out_arr, color, brick_length)
					current_brick[1] = brick_length + 1
					bricks.append(current_brick)
					current_brick = [0, 0, 0]
					brick_length = 0

				if col < num_cols - 1:
					if d.not_background(in_arr[row][col+1]):
						new_gaps.append(col) ## gap is to the right of the stored index

			elif v.color_mode == 0 and col < num_cols - 1 and not d.same_color(color, in_arr[row][col+1]) and d.not_background(in_arr[row][col+1]): # preserving img color, color switches
				d.end_brick(row, col, out_arr, color, brick_length+1)
				current_brick[1] = brick_length
				bricks.append(current_brick)
				current_brick = [0, 0, 0]
				brick_length = 0
				new_gaps.append(col)

			else: ## can keep extending brick
				d.continue_brick(row, col, out_arr, color)
				brick_length += 1

		# and col != num_cols - 1 why was this here?
		elif brick_length and not d.not_background(in_arr[row][col]): ## pixel is not colored and are currently drawing a brick
			if v.color_mode == 1:
				d.end_brick(row, col-1, out_arr, color, brick_length)
			elif v.color_mode == 0:
				d.end_brick(row, col-1, out_arr, in_arr[row][col-1], brick_length) # should make sure length + 1 is a possible length, use color of last pixel in brick
			current_brick[1] = brick_length
			bricks.append(current_brick)
			current_brick = [0, 0, 0]
			brick_length = 0

		elif brick_length and col == num_cols - 1:  ## drawing a brick and reach the rightmost column of the image
			d.end_brick(row, col, out_arr, color, brick_length)
			current_brick[1] = brick_length + 1
			bricks.append(current_brick)
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

if v.img_or_mujoco == 0:
	out_img = Image.fromarray(out_arr)
	out_img.save(f"lego-{v.image_path}")
	exit()

f = open("lego_model.xml", "w+")
f.write("<mujoco>\n  <worldbody>\n    <light pos=' 0 0 1'/>\n")
for brick in bricks:
	if color_type == "rgba":
		f.write(f'    <geom type="box" pos="0 {round(brick[0][1] * 0.1 + .05*brick[1], 2)} {round(brick[0][0] * -0.1, 2)}" size=".05 {round(.05 * brick[1], 2)} .05" rgba="{brick[2][0]/255} {brick[2][1]/255} {brick[2][2]/255} {brick[2][3]/255}"/>\n')
	elif color_type == "rgb":
		f.write(f'    <geom type="box" pos="0 {round(brick[0][1] * 0.1 + .05*brick[1], 2)} {round(brick[0][0] * -0.1, 2)}" size=".05 {round(.05 * brick[1], 2)} .05" rgba="{brick[2][0]/255} {brick[2][1]/255} {brick[2][2]/255} 1"/>\n')
f.write("  </worldbody>\n</mujoco>")
f.close()
print(bricks)
os.system("python -m mujoco.viewer --mjcf=./lego_model.xml")
# todo: make the above command work