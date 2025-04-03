import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    _, frame = video.read()
    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()




