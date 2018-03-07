import numpy as np
import cv2
from background import BackgroundRemover
from draw import Painter

cap = cv2.VideoCapture(0)


# t_minus = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)
# t = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
# t_plus = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

winName = "Movement Indicator"
win_name_diff = "Diff"
win_name_result = "Result"

cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

backgroud_diff = BackgroundRemover()

while(True):

    img_orig = cap.read()[1]
    gray = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)

    diff = backgroud_diff.diff(gray)

    diff = cv2.GaussianBlur(diff, (5,5), 0)

    ret, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    #thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.dilate(thresh, kernel, iterations=3)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    if len(contours) > 0:
        cnt = contours[0]
        Painter.draw_min_rect(img_orig, cnt)
        Painter.draw_rotated_rect(img_orig, cnt)
        Painter.draw_centroid(img_orig, cnt)
        cv2.line(img_orig, (80, 0), (80, img_orig.shape[0]), (255, 0, 0), 5)
        cv2.line(img_orig, (img_orig.shape[1] - 80, 0), (img_orig.shape[1] - 80, img_orig.shape[0]), (0, 0, 255), 3)

    cv2.imshow(win_name_diff, thresh)
    cv2.imshow(win_name_result, img_orig)

    # # Read next image
    # t_minus = t
    # t = t_plus
    # img_orig = cap.read()[1]
    # t_plus = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

