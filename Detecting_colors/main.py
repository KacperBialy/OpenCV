import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow("Mask")


def nothing(*args):
    pass


cv2.createTrackbar("B", "Mask", 0, 255, nothing)
cv2.createTrackbar("G", "Mask", 0, 255, nothing)
cv2.createTrackbar("R", "Mask", 0, 255, nothing)
cv2.createTrackbar("B_max", "Mask", 0, 255, nothing)
cv2.createTrackbar("G_max", "Mask", 0, 255, nothing)
cv2.createTrackbar("R_max", "Mask", 0, 255, nothing)
cv2.createTrackbar("Morphology", "Mask", 0, 1, nothing)
cv2.createTrackbar("kernel_morphology", "Mask", 0, 30, nothing)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, dsize=(600, 300))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    R = cv2.getTrackbarPos("R", "Mask")
    G = cv2.getTrackbarPos("G", "Mask")
    B = cv2.getTrackbarPos("B", "Mask")
    R_max = cv2.getTrackbarPos("R_max", "Mask")
    G_max = cv2.getTrackbarPos("G_max", "Mask")
    B_max = cv2.getTrackbarPos("B_max", "Mask")

    morphology_on_off = cv2.getTrackbarPos("Morphology", "Mask")
    kernel_morphology = cv2.getTrackbarPos("kernel_morphology", "Mask")

    lower_red = np.array([B, G, R])
    upper_red = np.array([B_max, G_max, R_max])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    cv2.imshow("hsv", hsv)
    cv2.imshow("Mask", mask)
    cv2.imshow("img", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
