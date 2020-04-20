import numpy as np
import cv2


def find_wall_x(img, threshold, square_x, matrix, x_start, y_start, x_size, y_size, grid, pixel_colision):
    b = 0
    labyrinth = np.copy(img)
    for j in range(grid):
        b += 1
        a = 0
        for i in range(grid - 1):
            a += 1
            sum_of_white_pixels = np.sum(threshold[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                                         x_start + i * square_x:x_size + x_start + (i + 1) * square_x])
            if sum_of_white_pixels > pixel_colision:
                labyrinth[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                x_start + i * square_x:x_size + x_start + (i + 1) * square_x] = (
                    0, 0, 255)
                matrix[j + b - 1, i + a] = 0
            else:
                labyrinth[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                x_start + i * square_x:x_size + x_start + (i + 1) * square_x] = (
                    0, 255, 0)
            cv2.imshow("rectangle", threshold[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                                    x_start + i * square_x:x_size + x_start + (i + 1) * square_x])
    cv2.imshow("img_x", labyrinth)
    cv2.waitKey(0)


def find_wall_y(img, threshold, square_x, matrix, x_start, y_start, x_size, y_size, grid, pixel_colision):
    b = 0
    labyrinth = np.copy(img)
    for j in range(grid - 1):
        b += 1
        a = 0
        for i in range(grid - 1):
            a += 1
            sum_of_white_pixels = np.sum(threshold[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                                         x_start + i * square_x:x_size + x_start + (i + 1) * square_x])
            if sum_of_white_pixels > pixel_colision:
                red = (0, 0, 255)
                labyrinth[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                x_start + i * square_x:x_size + x_start + (i + 1) * square_x] = red
                matrix[j + b, i + a - 1] = 0
            else:
                green = (0, 255, 0)
                labyrinth[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                x_start + i * square_x:x_size + x_start + (i + 1) * square_x] = green
            matrix[j + b, i + a + 1] = 0
            cv2.imshow("rectangle", threshold[y_start + j * square_x:(j + 1) * (square_x) + y_start + y_size,
                                    x_start + i * square_x:x_size + x_start + (i + 1) * square_x])
    cv2.imshow("img_y", labyrinth)
    cv2.waitKey(0)


def main():
    img = cv2.imread("./labirynt.jpg")
    cv2.imshow("img_original", img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    grid = 16
    square_x = int(img_gray.shape[0] / grid)

    _, threshold = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("threshold", threshold)

    x_start, y_start = (10, 6)
    x_size, y_size = (0, -15)
    matrix = np.ones(((grid - 1) * 2 + 1, (grid - 1) * 2 + 1), dtype='int')
    find_wall_x(img, threshold, square_x, matrix, x_start, y_start, x_size, y_size, grid, pixel_colision=30)

    x_start, y_start = (10, 6)
    x_size, y_size = (-15, 5)
    find_wall_y(img, threshold, square_x, matrix, x_start, y_start, x_size, y_size, grid, pixel_colision=30)
    print(matrix)

main()
