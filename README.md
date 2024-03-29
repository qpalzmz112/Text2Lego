# Text2Lego

Text2Lego is a Python program that takes a text prompt, passes it to an AI to generate images, and converts those images to buildable Lego designs (the bricks in the Lego designs are aligned in such a way that, were the design to be constructed physically, it would remain intact). The designs can be saved as images, or simulated in MuJoCo to test various physical properties. Here's an example:

Source image: 

<img src="https://github.com/qpalzmz112/Robot-Evolution-Simulator/assets/68213464/8c1932a0-c91c-4fbf-94eb-20e442dbf476" width="450" height="400">

Lego design with colors matching the source image:

<img src="https://github.com/qpalzmz112/Text2Lego/assets/68213464/318e1863-06ee-4713-94cf-5ab859533bbf" width="450" height="400">

Lego design in MuJoCo with colors matching the source image: (Although some of these bricks look very long, they are actually just adjacent bricks of the same color)

<img src="https://github.com/qpalzmz112/Text2Lego/assets/68213464/81d82f71-fe35-49bd-8c45-2ce290283ba3" width="450" height="400">

Lego design with random colors:

<img src="https://github.com/qpalzmz112/Robot-Evolution-Simulator/assets/68213464/21d93a20-e995-464d-a1ef-4396de03613d" width="450" height="400">

Lego design in MuJoCo with random colors:

<img src="https://github.com/qpalzmz112/Robot-Evolution-Simulator/assets/68213464/76670ead-aee0-41af-b2d0-a31f2dad5d30" width="450" height="400">


In the `variables.py` file, there are the following options:
- add a filepath to an image if you just want to convert an image to a buildable Lego design
- choose between the Lego design matching brick colors to the colors in the image, or randomly coloring bricks using colors from the Lego color palette. If Text2Lego is
preserving the image's original colors, it will account for this when creating the Lego design, i.e., Text2Lego will adjust the bricks in the Lego design so that the colors
in the design match those of the source image.
- output the Lego design as an image or simulate it in MuJoCo, or both

## To do:
- make Lego design generation more robust - as of now, it only supports a fixed set of brick lengths: {1, 2, 3, 4}. This should at least support the longer bricks that Lego produces.
- add a GUI so that Text2Lego is easier to use
- find a suitable image-generation AI to use
- add a way to differentiate adjacent bricks of the same color in MuJoCo
