# coding:utf-8
import os
# import tesserocr
# from PIL import Image

try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract
import logging


CHARACTER_SET = 'eng'
# DEFAULT_SEGMENT_MODE = tesserocr.PSM.SINGLE_LINE
DEFAULT_SEGMENT_MODE = '-psm 7'

class OcrDetector:
    def __init__(self, is_chi_sim):
        self.is_chi_sim = is_chi_sim

    # @staticmethod
    def set_lang(self, is_chi_sim):
        self.is_chi_sim = is_chi_sim
        if is_chi_sim:
            logging.info('OCR detect character: chinese simple')
        else:
            logging.info('OCR detect character: english')

    def detect(self, binary_file_name):
        binary = Image.open(binary_file_name)
        # return tesserocr.image_to_text(binary, lang = DEFAULT_CHARACTER_SET, psm = DEFAULT_SEGMENT_MODE)
        if self.is_chi_sim:
            CHARACTER_SET = 'chi_sim'
        else:
            CHARACTER_SET = 'eng'
        txt = pytesseract.image_to_string(binary, lang=CHARACTER_SET, config=DEFAULT_SEGMENT_MODE)

        # print pytesseract.image_to_string(binary, 'chi_sim', True, DEFAULT_SEGMENT_MODE)
        # if txt is None:
        #     txt = pytesseract.image_to_string(binary, lang=DEFAULT_CHARACTER_SET, config=DEFAULT_SEGMENT_MODE)
        return txt

    # def detect_text_and_coordinate(self, binary_file_name):
    #     image = Image.open(binary_file_name)
    #
    #     if self.is_chi_sim:
    #         CHARACTER_SET = 'chi_sim'
    #     else:
    #         CHARACTER_SET = 'eng'
    #
    #     with tesserocr.PyTessBaseAPI() as api:
    #         api.SetImage(image)
    #         boxes = api.GetComponentImages(tesserocr.RIL.TEXTLINE, True)
    #         print 'Found {} textline image components.'.format(len(boxes))
    #         for i, (im, box, _, _) in enumerate(boxes):
    #             # im is a PIL image object
    #             # box is a dict with x, y, w and h keys
    #             api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
    #             ocrResult = api.GetUTF8Text()
    #             conf = api.MeanTextConf()
    #             print (u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
    #                    "confidence: {1}, text: {2}").format(i, conf, ocrResult, **box)
    #
    # def detect_single_word(self, binary_file_name):
    #     binary = Image.open(binary_file_name)
    #
    #     if self.is_chi_sim:
    #         CHARACTER_SET = 'chi_sim'
    #     else:
    #         CHARACTER_SET = 'eng'
    #
    #     return tesserocr.image_to_text(binary, CHARACTER_SET)

# import cv2
# import uuid
#
# color = cv2.imread("055f1d30-4481-4dec-b306-9b95ff528887.png",cv2.IMREAD_COLOR)
# grey = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
# ret, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# binary_file_name = str(uuid.uuid4()) + ".png"
# cv2.imwrite(binary_file_name, binary)
# cv2.imshow("binary", binary)
# cv2.waitKey(300)
#
# h=binary.shape[0]
# w=binary.shape[1]
# print "h=", h, "w=", w
# ct, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#
# print binary[0][0]
# print binary[h-1][0]
# print binary[0][w-1]
# print binary[h-1][w-1]
#
# print binary[0][(w-1)/2]
#
#
#
# # remove_list = []
# # for c in contours:
# #     m = cv2.moments(c)
# #     cx = int(m['m10'] / m['m00'])
# #     cy = int(m['m01'] / m['m00'])
# #
# #     if abs(cx - w) <= 3 or abs(cy - h)<=3:
# #         remove_list.append(c)
# #     elif abs(cx - 0) <=3 or abs(cy - 0) <=3:
# #         remove_list.append(c)
# #     print cx, cy
#
# txt = pytesseract.image_to_string(binary, lang=DEFAULT_CHARACTER_SET, config=DEFAULT_SEGMENT_MODE)
#
#
# #
# #
# #
# ocr = OcrDetector(True)
# t =ocr.detect("/root/workspace/devicepass-ai/auto_login/test_xml_img/1.png")
# print t
#
#
# import numpy as np
# import cv2
#
# image = cv2.imread('2b37128c-f4be-4884-8478-6153699834be.png')
# a,b,c = image[0,0,:]
# a = [int(a),int(b),int(c)]
# diff =2
# h,w = image.shape[:2]
# cv2.rectangle(image,(0,0),(w-1,h-1),(a[0],a[1],a[2]),3)
# flooded = image.copy()
# mask = np.zeros((h+2,w+2),np.uint8)
# print image[0,0,:]
# cv2.floodFill(flooded,mask,(1,h/2-1),(255-a[0],255-a[1],255-a[2]),diff,diff)
#
# #canny = cv2.Canny(image,30,150)
# #canny = np.uint8(np.absolute(canny))
# cv2.imwrite('111.jpg',flooded)