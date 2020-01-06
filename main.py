import cv2
import pygame
import random


def draw_objects_on_screen(rectangles, screen):
    for rect in rectangles:
        pygame.draw.rect(screen, (255, 255, 255), rect)


def check_collision(pointer, rectangles):
    for i in range(len(rectangles)):
        if rectangles[i].colliderect(pointer):
            rectangles[i].y -= random.randrange(500, 1200)


def rain_of_squares(rectangles):
    for i in range(len(rectangles)):
        rectangles[i].y += 10
        if rectangles[i].y > 600:
            rectangles[i].y -= random.randrange(500, 1200)


def main():
    capture = cv2.VideoCapture(0)

    size = width_of_window, height_of_window = 800, 600
    screen = pygame.display.set_mode(size)

    rectangles = []
    for i in range(10):
        rectangle = pygame.Rect(random.randrange(70, width_of_window - 70), -random.randrange(0, 1000), 35, 35)
        rectangles.append(rectangle)

    timer = pygame.time.Clock()
    while True:
        timer.tick()
        print(timer.get_fps())
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame_copy = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        (min_Val, max_Val, min_Loc, max_Loc) = cv2.minMaxLoc(gray)

        # cv2.circle(frame_copy, max_Loc, 5, (255, 0, 0), 2)
        # cv2.imshow('frame', frame_copy)

        height_of_frame, width_of_frame = frame_copy.shape[0:2]
        location_of_square = max_Loc[0] * width_of_window // width_of_frame, max_Loc[
            1] * height_of_window // height_of_frame

        pointer = pygame.Rect(location_of_square[0], location_of_square[1], 40, 40)
        check_collision(pointer, rectangles)

        screen.fill((0, 0, 0))

        draw_objects_on_screen(rectangles, screen)

        pygame.draw.rect(screen, (255, 255, 255), pointer)

        rain_of_squares(rectangles)

        pygame.display.flip()
        key = cv2.waitKey(1)
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()
