from thumbor.filters import BaseFilter, filter_method
from thumbor.loaders.http_loader import *
import numpy as np
import cv2


class Filter(BaseFilter):
    @filter_method()
    def borders(self):
        img = np.array(self.engine.image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_border = gray - gray[0][0]
        im2, contours, hierarchy = cv2.findContours(gray_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        try:
            hierarchy = hierarchy[0]
        except:
            hierarchy = []
        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        for contour, hier in zip(contours, hierarchy):
            (x, y, w, h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)
        if abs(min_y - height + max_y) >= 0 and abs(min_y - height + max_y) < 2 \
                and abs(min_x - width + max_x) >= 0 and abs(min_x - width + max_x) < 2 and \
                (height - max_y != 0 or width - max_x != 0):  # Checking for error of one pixel
            self.engine.crop(min_x, min_y, max_x, max_y)
        else:
            self.engine.resize(width, height)
