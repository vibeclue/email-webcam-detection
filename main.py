import glob
import os

import cv2
import time

from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
counter = 0


def clean_folder():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)


while True:
    status = 0
    _, frame = video.read()  # получаю frame

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # создаю серый фрейм
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0) # блюр
    # теперь изображение вебки серое и размытое : cv2.imshow('Video', gray_frame_gau)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau) # вычитается разница между самый первым кадром и теми что отображаются

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]  # делаю более жесткие границы между белым и черным
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # cv2.imshow('Video1', dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #  контур прямоугольника на объекте, который появляется в кадре
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)

        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if rectangle.any():
            status = 1

            cv2.imwrite(f'images/{counter}.png', frame)
            counter += 1
            all_images = glob.glob("images/*.png")

            image_with_object = all_images[len(all_images) // 2]

    status_list.append(status)
    status_list = status_list[-2:]

    # в status_list когда ничего не происходит, будут нули [0, 0]
    # когда в кадре появится прямоугольник, будет [1, 1]
    # в момент когда прямоугольник исчезнет, будет [1, 0], и в этот момент произойдет отправка фото
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))  # использование многопоточности
        email_thread.daemon = True
        # send_email(image_with_object)
        clean_thread = Thread(target=clean_folder)  # использование многопоточности
        clean_thread.daemon = True
        # clean_folder()

        email_thread.start()
        # clean_thread.start()


    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()

clean_thread.start()  # будет чиститься когда выйти из проги




