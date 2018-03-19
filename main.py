import numpy as np
import cv2
from background import BackgroundRemover
from draw import Painter
from interceptor import Interceptor

cap = cv2.VideoCapture(0)

win_name_diff = "Movement Indicator"
win_name_result = "Result"

cv2.namedWindow(win_name_diff, cv2.WINDOW_AUTOSIZE)

backgroud_diff = BackgroundRemover()

img_size = cap.read()[1].shape
entrace = {'init': (80, 0), 'end': (80, img_size[0])}
exit = {'init': (img_size[1] - 80, 0), 'end': (img_size[1] - 80, img_size[0])}

entrace_interceptor = Interceptor(entrace)
exit_interceptor = Interceptor(exit)
last_centroid = None

blue = (255, 0, 0)
red = (0, 0, 255)
min_width = 80
min_heigth = 150

while True:

    img_orig = cap.read()[1]
    gray = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)

    diff = backgroud_diff.diff(gray)

    diff = cv2.GaussianBlur(diff, (5, 5), 0)

    ret, thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.dilate(thresh, kernel, iterations=3)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for (i, cnt) in enumerate(contours):
        #cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)
        contour_valid = (w >= min_width) and (h >= min_heigth)
        if not contour_valid:
            continue
        #if w < 100 and h > 100:
        Painter.draw_min_rect(img_orig, cnt)
        Painter.draw_rotated_rect(img_orig, cnt)
        # Painter.draw_centroid(img_orig, cnt)
        centroid = Painter.get_centroid(cnt)
        if centroid is not None and last_centroid is not None:
            entrace_interceptor.evaluate(centroid, last_centroid)
            exit_interceptor.evaluate(centroid, last_centroid)
        last_centroid = centroid

    cv2.line(img_orig, entrace['init'], entrace['end'], blue, 5)
    cv2.line(img_orig, exit['init'], exit['end'], red, 3)
    cv2.putText(img_orig, 'Entrada: {}'.format(entrace_interceptor.counter),
                (0, 50), cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=blue, thickness=2)
    cv2.putText(img_orig, 'Saida: {}'.format(exit_interceptor.counter),
                (400, 50), cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=red, thickness=2)

    cv2.imshow(win_name_diff, thresh)
    cv2.imshow(win_name_result, img_orig)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
