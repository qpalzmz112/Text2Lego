from PIL import Image
import numpy as np
from numpy import asarray
import variables as v
import draw as d

in_img = Image.open(v.image_path)
in_arr = asarray(in_img)
num_cols, num_rows = in_img.size

if v.image_type == "png":
	color_len = 4 ## rgba
elif v.image_type ==  "jpg":
	color_len = 3 ## rgb

out_arr = np.full((4*num_rows, 4*num_cols, color_len), 255, dtype = np.uint8)

max_len = max(v.brick_lengths)
for row in range(num_rows):
	counter = 0
	for col in range(num_cols):
		color = in_arr[row][col]

		# if color and not started:
		#	start brick, save start
		# if started and color:
		#	length += 1, continue brick
		# if started and length = max length:
		#	end brick
		#   if next pixel is color:
		#		store brick gap
		# if started and not color:
		#	if length is a brick length:
		#		end brick
		#	else:
		#		end brick one back

		if d.not_background(color) and not counter:
			d.start_brick(row, col, out_arr, color)
			counter = 1
			start_col = col

		elif d.not_background(color) and counter:
			if counter + 1 == max_len:
				# if gap, can't end here; need to make a shorter brick of possible length
				d.end_brick(row, col, out_arr, color)
				counter = 0
			else:
				d.continue_brick(row, col, out_arr, color)
				counter += 1
		elif counter:
			d.end_brick(row, col-1, out_arr, color) # should make sure counter + 1 is a possible length
			counter = 0


for col in range(num_cols):
	brick = False
	for row in range(1, num_rows):
		if d.not_background(in_arr[row][col]) and not brick:
			d.draw_stud(row - 1, col, out_arr)
			brick = True
		else:
			brick = False


out_img = Image.fromarray(out_arr)
out_img.show()