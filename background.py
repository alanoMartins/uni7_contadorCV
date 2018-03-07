import cv2


class BackgroundRemover:

    def __init__(self, method=0):
        self.method = method
        self.gmm_diff = cv2.createBackgroundSubtractorMOG2()

    def diff(self, *frame):
        if self.method == 0:
            return self.__gmm_diff(frame[0])
        else:
            return self.__substract_diff(frame[0], frame[1], frame[2])

    def __gmm_diff(self, frame):
        return self.gmm_diff.apply(frame)

    def __substract_diff(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)
