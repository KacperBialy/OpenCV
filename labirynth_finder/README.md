
First step:

we need to convert the original image to a binary image, where the background is black and the walls are white.
This will allow later calculations.

![threshold](https://user-images.githubusercontent.com/44371092/79797828-42d77a80-8358-11ea-9a4b-a2002a4f987c.jpg)

Second step:

we search each field in the maze in the x axis using a rectangle, if the rectangle intersects the wall,
it changes its color to red and writes the wall positions in the appropriate place of the matrix.

![img_x](https://user-images.githubusercontent.com/44371092/79797836-466b0180-8358-11ea-9016-7ed0bcd2b0a6.jpg)


Third step:
Do the same with the y axis.

![img_y](https://user-images.githubusercontent.com/44371092/79797843-4965f200-8358-11ea-8dfe-d64015923aa5.jpg)

Result:
![result](https://user-images.githubusercontent.com/44371092/79801116-cf386c00-835d-11ea-9e48-28ef807af7c1.png)
