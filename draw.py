import cv2
import numpy as np


class Painter:

    @staticmethod
    def draw_min_rect(frame, cnt):
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    @staticmethod
    def draw_rotated_rect(frame, cnt):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

    @staticmethod
    def draw_centroid(frame, cnt):
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(frame, (cx, cy), 3, (255, 0, 0))

    @staticmethod
    def get_centroid(cnt):
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return cx, cy

    @staticmethod
    def draw_entrace(frame):
        cv2.line(frame, (80, 0), (80, frame.shape[0]), (255, 0, 0), 5)

    @staticmethod
    def draw_exit(frame):
        cv2.line(frame, (frame.shape[1] - 80, 0), (frame.shape[1] - 80, frame.shape[0]), (0, 0, 255), 3)

