import random

import cv2
import numpy as np
import operator
import serial
import time

ser = serial.Serial()


def find_biggest_grid(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]


def crop_and_warp(img, crop_rect):
    top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]
    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')
    dst = np.array([[0, 0], [576, 0], [576, 576], [0, 576]], dtype='float32')
    H = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, H, (576, 576))


def find_board(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    B = 31;
    G = 0;
    R = 71;
    B_max = 100;
    G_max = 163;
    R_max = 255;
    lower_red = np.array([B, G, R])
    upper_red = np.array([B_max, G_max, R_max])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours = find_biggest_grid(mask)
    board = crop_and_warp(image, contours)
    return board


def find_ball_x_y(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
    return [polygon[top_left][0], polygon[bottom_right][0]]


def configurate_port():
    ser.baudrate = 9600
    ser.port = 'COM10'
    ser.parity = 'N'
    ser.stopbits = 1
    ser.bytesize = 8
    ser.open()


def send_string_uart(text_to_send):
    for i in range(len(text_to_send)):
        byte = text_to_send[i:i + 1].encode()
        ser.write(byte)


def find_ball_position(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    B = 0;
    G = 0;
    R = 90;
    B_max = 31;
    G_max = 255;
    R_max = 255;
    lower_red = np.array([B, G, R])
    upper_red = np.array([B_max, G_max, R_max])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    top_left, top_right = find_ball_x_y(mask)
    return top_left, top_right


cap = cv2.VideoCapture(1)

game = np.zeros((576, 576, 3))

x, y = (300, 300)


def main():
    global x, y

    # configurate_port()
    # x_pos = 0
    # y_pos = 0
    # x_pos_string = ""
    # y_pos_string = ""
    # t0 = time.time()
    while True:
        try:
            _, frame = cap.read()
            board = find_board(frame)
            board_squares = np.copy(board)
            top_left, bottom_right = find_ball_position(board)
            sum_of_white_pixels = np.sum(game[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]])
            if sum_of_white_pixels > 10000:
                print(sum_of_white_pixels)
                game[x:x + 60, y:y + 60] = (0, 0, 0)
                x = random.randrange(50, 526)
                y = random.randrange(50, 526)
            else:
                game[x:x + 60, y:y + 60] = (255, 255, 255)
                game[x:x + 60, y:y + 60] = (255, 255, 255)
                board_squares[x:x + 50, y:y + 50] = (0, 255, 0)
            cv2.imshow("frame", frame)
            cv2.imshow("board_squares", board_squares)
            cv2.imshow("ball", board[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]])

        except:
            print('Couldnt find ball!')
        # t1 = time.time()
        # total = t1 - t0
        # if total > 10:
        #     x_pos = int((top_left[0] + bottom_right[0]) / 2)
        #     x_pos_string = str(x_pos)
        #     if len(x_pos_string) == 2:
        #         x_pos_string = "0" + x_pos_string
        #     if len(x_pos_string) == 1:
        #         x_pos_string = "00" + x_pos
        #
        #     y_pos = int((top_left[1] + bottom_right[1]) / 2)
        #     y_pos_string = str(y_pos)
        #     if len(y_pos_string) == 2:
        #         y_pos_string = "0" + y_pos_string
        #     if len(x_pos_string) == 1:
        #         y_pos_string = "00" + y_pos
        #     send_string_uart(x_pos_string + y_pos_string)
        cv2.waitKey(1)


main()