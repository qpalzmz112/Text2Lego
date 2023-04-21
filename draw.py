import variables as v

if v.image_type == "png":
	border = [174, 109, 226, 153] ## a nice lilac color
elif v.image_type == "jpg":
	border = [108, 68, 140]


## The draw functions take in a pixel coordinate from
## the input image, and use that as the top left coordinate
## for the 4x4 grid each pixel is mapped to in the output image
def start_brick(row, col, arr, color):
	row *= 4
	col *= 4
	if v.color_mode == 1:
		border_color = color
	elif v.color_mode == 0:
		border_color = border

	for i in range(4):
		arr[row][col+i] = border_color
		arr[row+3][col+i] = border_color
		arr[row+i][col] = border_color
		if i > 0:
			arr[row+1][col+i] = color
			arr[row+2][col+i] = color

def continue_brick(row, col, arr, color):
	row *= 4
	col *= 4
	if v.color_mode == 1:
		border_color = color
	elif v.color_mode == 0:
		border_color = border

	for i in range(4):
		arr[row][col+i] = border_color
		arr[row+3][col+i] = border_color
		arr[row+1][col+i] = color
		arr[row+2][col+i] = color

def end_brick(row, col, arr, color, brick_length):
	row *= 4
	col *= 4
	if v.color_mode == 1:
		border_color = color
	elif v.color_mode == 0:
		border_color = border

	for i in range(0, 4):
		arr[row][col+i] = border_color
		arr[row+3][col+i] = border_color
		arr[row+i][col+3] = border_color
		if i < 3:
			if i != 0 or brick_length != 1:
				arr[row+1][col+i] = color
				arr[row+2][col+i] = color

def draw_stud(row, col, arr, color=[-1]):
	row *= 4
	col *= 4
	if color[0] != -1:
		border_color = color
	else:
		border_color = border

	arr[row+3][col+1] = border_color
	arr[row+3][col+2] = border_color

def not_background(arr):
	if v.image_type == "png": 
		if arr[0] == 0 and arr[1] == 0 and arr[2] == 0: ## rgba: [0,0,0,0] is transparent, [0,0,0,255] is black
			return arr[3] != 0 ## return true if pixel is not transparent
		else:
			return True
	elif v.image_type == "jpg":
		return arr[0] != 255 or arr[1] != 255 or arr[2] != 255 ## return true if color is not pure white

def same_color(color1, color2):
	for (num1, num2) in zip(color1, color2):
		if num1 != num2:
			return False
	return True

