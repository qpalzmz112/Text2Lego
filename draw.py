## The draw functions take in a pixel coordinate from
## the input image, and use that as the top left coordinate
## for the 4x4 grid each pixel is mapped to in the output image

def start_brick(row, col, arr):
	color = [0,0,0,255]
	row *= 4
	col *= 4
	for i in range(4):
		arr[row][col+i] = color
		arr[row+3][col+i] = color
		arr[row+i][col] = color

def continue_brick(row, col, arr):
	color = [0,0,0,255]
	row *= 4
	col *= 4
	for i in range(4):
		arr[row][col+i] = color
		arr[row+3][col+i] = color

def end_brick(row, col, arr):
	color = [0,0,0,255]
	row *= 4
	col *= 4
	for i in range(4):
		arr[row][col+i] = color
		arr[row+3][col+i] = color
		arr[row+i][col+3] = color

def draw_stud(row, col, arr):
	color = [0,0,0,255]
	row *= 4
	col *= 4
	arr[row+3][col+1] = color
	arr[row+3][col+2] = color

def not_background(arr):
	return arr[0] == 0 and arr[1] == 0 and arr[2] == 0 and arr[3] == 255