from thumbor.filters import BaseFilter, filter_method
from thumbor.loaders.http_loader import *
import numpy as np
import cv2

class Filter(BaseFilter):

    @filter_method()
    def borders(self):
        engine = self.context.modules.engine
        mode, data = self.engine.image_data_as_rgb()
        gray_border = []                                   #Gray_border is used to get black borders only
        img=np.array(self.engine.image) 
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray_border = gray - gray[0][0]
        #imageandedges=cv2.add(edged,gray_border)
        im2, contours, hierarchy = cv2.findContours(gray_border,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        try: hierarchy = hierarchy[0]
        except: hierarchy = []
        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        for contour, hier in zip(contours, hierarchy):
            (x, y, w, h)= cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x+w, max_x)
            min_y, max_y = min(y, min_y), max(y+h, max_y)
        if abs((height-max_y)-min_y)<10 and abs((width-max_x)-min_x)<10:
            self.engine.crop(min_x,min_y,max_x,max_y)
            return 

        #if abs(min_y-height+max_y)<7:
        if abs((height-max_y)-min_y)<10:
         # Checking for error of one pixel
            self.engine.crop(0,min_y,width,max_y)
            return

        #if abs(min_x-width+max_x)<7:
        if abs((width-max_x)-min_x)<10:
            self.engine.crop(min_x,0,max_x,height)
            return
