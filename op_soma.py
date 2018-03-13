import numpy as np
import cv2

yoda = cv2.imread('imagens/yoda.jpg')
yoda2 = cv2.add(yoda, 100)

cv2.imshow('imageWindow', yoda)
cv2.imshow('ImageWindow',yoda2)
cv2.imwrite('imagens/yoda2.jpg',yoda2)

cv2.waitKey(0)
cv2.destroyAllWindows()


