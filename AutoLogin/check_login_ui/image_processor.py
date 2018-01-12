# coding:utf-8
import cv2
import ocr_detector
import numpy as np
import uuid
import helper
import os
import logging
# import matplotlib.pyplot as plt
# from matplotlib import animation

TEMP_FILE_PATH = "./"


class ImageProcessor:
    def __init__(self, is_chi_sim):
        self.tess_ocr = ocr_detector.OcrDetector(is_chi_sim)

    def set_language(self, is_chi_sim):
        self.tess_ocr.set_lang(is_chi_sim)

    def read_screen_img(self, img_url):
        screen_img_color = cv2.imread(img_url, cv2.IMREAD_COLOR)
        if screen_img_color is None:
            logging.critical('Read image file FAILURE!!!')
            return None, 0, 0

        self.height = screen_img_color.shape[0]
        self.width  = screen_img_color.shape[1]

        if screen_img_color is None:
            return None, 0, 0
        else:
            return screen_img_color, self.height, self.width

    def coord_transform(self, coord):
        # logging.info(type(coord), coord)
        coord = coord.strip('[').strip(']').split('][')
        coord_list = list(coord)
        return coord_list

    def crop(self, screen_img_color, coord):
        if screen_img_color is None:
            return  False

        coord_list = self.coord_transform(coord)
        left_top = coord_list[0].split(',')
        right_down = coord_list[1].split(',')

        left = int(left_top[0]);    upper = int(left_top[1])
        right = int(right_down[0]); down = int(right_down[1])
        cropped = screen_img_color[upper:down, left:right, :]

        return True, cropped

    def crop2(self, img_gray, coord):
        if img_gray is None:
            return  False

        coord_list = self.coord_transform(coord)
        left_top = coord_list[0].split(',')
        right_down = coord_list[1].split(',')

        left = int(left_top[0]);    upper = int(left_top[1])
        right = int(right_down[0]); down = int(right_down[1])
        cropped = img_gray[upper:down, left:right]

        return True, cropped

    def angle_from_right(self, deg):
        return min(deg % 90, 90 - (deg % 90))

    def remove_border(self, contour, ary):
        c_im = np.zeros(ary.shape)
        r = cv2.minAreaRect(contour)
        degs = r[2]
        if self.angle_from_right(degs) <= 10.0:
            box = cv2.cv.BoxPoints(r)
            box = np.int0(box)
            cv2.drawContours(c_im, [box], 0, 255, -1)
            cv2.drawContours(c_im, [box], 0, 0, 4)
        else:
            x1, y1, x2, y2 = cv2.boundingRect(contour)
            cv2.rectangle(c_im, (x1, y1), (x2, y2), 255, -1)
            cv2.rectangle(c_im, (x1, y1), (x2, y2), 0, 4)

        return np.minimum(c_im, ary)

    def show_img(self, screen_img_color, coord):
        img_show = screen_img_color.copy()
        coord_list = self.coord_transform(coord)
        left_top = coord_list[0].split(',')
        right_down = coord_list[1].split(',')

        left = int(left_top[0]);    upper = int(left_top[1])
        right = int(right_down[0]); down = int(right_down[1])

        cv2.rectangle(img_show, (left, upper), (right, down), (0, 0, 255), 2, 8)

        # cv2.namedWindow("widget shot", cv2.WINDOW_NORMAL)
        # cv2.imshow("widget shot", img_show)
        # cv2.waitKey(0)

    def convert_greyscale(self, cropped_img_color):
        cropped_img_grey = cv2.cvtColor(cropped_img_color, cv2.COLOR_BGR2GRAY)
        return cropped_img_grey

    def process_exception(self, binary):
        # print binary.shape,'=================='
        a= binary[0, 0]
        a = [int(a), int(a), int(a)]
        diff = 2
        h, w = binary.shape[:2]
        cv2.rectangle(binary, (0, 0), (w - 1, h - 1), (a[0], a[1], a[2]), 3)
        flooded = binary.copy()
        mask = np.zeros((h + 2, w + 2), np.uint8)
        # print image[0, 0, :]
        cv2.floodFill(flooded, mask, (1, h / 2 - 1), (255 - a[0], 255 - a[1], 255 - a[2]), diff, diff)

        return flooded

    def binary_most_black_pixels(self, binary):
        most_black = False
        num_black = num_white = 0

        for i in range(binary.shape[0]):
            for j in range(binary.shape[1]):
                if binary[i][j] == 0:
                    num_black = num_black + 1
                elif binary[i][j] == 255:
                    num_white = num_white + 1

        if num_black > num_white:
            most_black = True

        return most_black

    def hist_projection(self, most_black, binary):

        PIX_VAL = 0
        if most_black:
            PIX_VAL = 255
        else:
            PIX_VAL = 0

        # X axis projection
        dict_col_pixels = []
        for j in range(binary.shape[1]):
            num_col_pix = 0
            for i in range(binary.shape[0]):
                if binary[i][j] == PIX_VAL:
                    num_col_pix = num_col_pix + 1
            # dict_col_pixels[j] = num_col_pix
            dict_col_pixels.append(num_col_pix)

        # Y axis projection
        dict_row_pixels = []
        for i in range(binary.shape[0]):
            num_row_pix = 0
            for j in range(binary.shape[1]):
                if binary[i][j] == PIX_VAL:
                    num_row_pix = num_row_pix + 1
            # dict_row_pixels[i] = num_row_pix
            dict_row_pixels.append(num_row_pix)

        return dict_col_pixels, dict_row_pixels

    def count_pixels(self, binary, most_black):
        return self.hist_projection(most_black, binary)

    def smooth_curve(self, pixel_list, curve_width):
        l1 = l2 = pixel_list

        ITER_NUM = 1
        iter = 0
        while iter < ITER_NUM:
            l2[0] = (l1[0] + l1[0] + l1[1]) / 3
            for y in range(1, curve_width):
                # l2[y] = (l1[y - 1] + l1[y] + l1[y + 1]) / 3
                l2[y-1] = (l1[y - 2] + l1[y-1] + l1[y]) / 3
            l2[curve_width-1] = (l1[curve_width-2] + l1[curve_width-1] + l1[curve_width-1]) / 3
            iter = iter+1

        return l2

    def smooth_curve2(self, pixel_list, curve_width):
        l1 = l2 = pixel_list

        # ITER_NUM = 1
        iter = 0
        # while iter < ITER_NUM:
        l2[0] = (l1[0] + l1[0] + l1[1]) / 3
        for y in range(1, curve_width):
            # l2[y] = (l1[y - 1] + l1[y] + l1[y + 1]) / 3
            l2[y-1] = (l1[y - 2] + l1[y-1] + l1[y]) / 3
        l2[curve_width-1] = (l1[curve_width-2] + l1[curve_width-1] + l1[curve_width-1]) / 3
        # iter = iter+1

        return l2


    # def smooth_xy_curves(self, x_pixels, y_pixels):
    #     self.smooth_curve(x_pixels)
    #
    #     plt.subplot(221), plt.plot(dict_col_pixels)
    #     plt.subplot(223), plt.imshow(binary, 'binary')
    #     plt.subplot(224), plt.plot(dict_row_pixels)
    #     # plt.xlabel('X & Y Axis')
    #     # plt.ylabel('Pixel Numbers')
    #     plt.show()

    def crop_logon_btn_img(self, cropped_img_grey):
        h = cropped_img_grey.shape[0]
        w = cropped_img_grey.shape[1]

        w_ratio = 0.2
        h_ratio = 0.3

        strip_w = w * w_ratio * 0.5
        strip_h = h * h_ratio * 0.5
        left = int(strip_w)
        upper = int(strip_h)
        right = int(w - strip_w)
        down = int(h - strip_h)
        coord1 = []; coord2 = []
        coord1.append(left);  coord1.append(upper)
        coord2.append(right); coord2.append(down)
        str_coord = '['+ str(left)+','+str(upper)+']['+str(right)+','+str(down)+']'

        rc, cropped_color = self.crop2(cropped_img_grey, str_coord)

        return cropped_color

    def pre_processing(self, is_logon_btn, cropped_color, screen_width):
        if cropped_color is None:
            return False

        # color_file_name = str(uuid.uuid4()) + ".jpg"
        # # cv2.imshow("color_cropped", cropped_color)
        # # cv2.waitKey(0)
        # cv2.imwrite(color_file_name, cropped_color)

        cropped_img_grey = self.convert_greyscale(cropped_color)

        if is_logon_btn:
            '''如果是登录按钮，可裁剪边框'''
            cropped_w = cropped_img_grey.shape[1]
            if cropped_w >  screen_width * 0.15:
                cropped_img_grey = self.crop_logon_btn_img(cropped_img_grey)

        # h = binary.shape[0]
        # w = binary.shape[1]
        #
        # top_left_value = binary[0][0]
        # left_down_value = binary[h - 1][0]
        # right_top_value = binary[0][w - 1]
        # rigth_down_value = binary[h - 1][w - 1]
        # top_middle_value = binary[0][(w-1)/2]
        # middle_value = binary[(h-1)/2][(w-1)/2]
        #
        # # print ( "top_left_value: ", top_left_value,
        # # "left_down_value: ", left_down_value,
        # # "right_top_value: ", right_top_value,
        # # "rigth_down_value: ",rigth_down_value,
        # # "top_middle_value: ", top_middle_value,
        # #         "middle_value: ", middle_value)
        #
        # if (top_left_value == left_down_value and left_down_value == right_top_value and  right_top_value== rigth_down_value
        #     # and top_left_value != top_middle_value):
        #     and top_left_value != middle_value):
        #     binary = self.process_exception(binary)

        ret, binary = cv2.threshold(cropped_img_grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        binary_file_name = str(uuid.uuid4()) + ".jpg"
        cv2.imwrite(binary_file_name, binary)

        # cv2.imshow("binary", binary)
        # cv2.waitKey(0)

        return binary_file_name


    def process_and_detect(self, is_logon_btn, cropped_color, screen_width):
        # logging.info( "ocr detect...")

        if cropped_color is None:
            return False

        if self.tess_ocr is None:
            return False

        self.binary_file_name = self.pre_processing(is_logon_btn, cropped_color, screen_width)

        txt = self.tess_ocr.detect(self.binary_file_name)

        return txt
        # return self.tess_ocr.detect_single_word(self.binary_file_name)


    # def enhancement(self, gray, fa, fb):
    #     enhanced = cv2.CreateImage(cv2.GetSize(gray), gray.depth, 1)
    #     k = 255 /(fb - fa)
    #     for i in range(gray.height):
    #         for j in range(gray.width):
    #             if (gray[j, i] < fa):
    #                 enhanced[j, i]= 0
    #             elif (gray[j, i] > fb):
    #                 enhanced[j, i] = 255
    #             else:
    #                 enhanced[j, i] = k * (gray[j, i] - fa)
    #     return enhanced

    def estimate_widgets(self,is_logon_btn, screen_img_color, key_list, candidate_widget_list):

        # img_proc = image_processor.ImageProcessor()
        # rc, screen_img_color = img_proc.read_screen_img(shot_img_url)
        # if not rc:
        #     return False

        # logging.info( ">>>>>>>>>>>>>>>>estimate widget")
        widget_list = []
        for candit in candidate_widget_list:
            coord = candit.get('bounds')
            # print coord
            coord_list = self.coord_transform(coord)
            left_top = coord_list[0].split(',')
            right_down = coord_list[1].split(',')

            left = int(left_top[0])
            upper = int(left_top[1])
            right = int(right_down[0])
            down = int(right_down[1])

            if abs(left - right) < 10 or abs(upper - down) < 10:
                continue

            self.show_img(screen_img_color, coord)

            rc, cropped_color = self.crop(screen_img_color, coord)
            if not rc:
                continue
            screen_width = screen_img_color.shape[1]
            result = self.process_and_detect(is_logon_btn, cropped_color, screen_width)

            if os.path.exists(self.binary_file_name):
                os.remove(self.binary_file_name)

            if not helper.check_ocr_detect_result(is_logon_btn, key_list, result):
                continue
            else:
                widget_list.append(candit)
        logging.info("estimate widget<<<<<<<<<<<<<<<")

        return widget_list

    def ocr_detect(self, is_logon_btn, shot_img_url, key_list, widgets):
        is_chinese_sim = False
        eng_ocr_detect_failure = False
        for i in range(0, 2):
            if eng_ocr_detect_failure:
                is_chinese_sim = True
            self.set_language(is_chinese_sim)
            screen_img_color, height, width = self.read_screen_img(shot_img_url)
            if screen_img_color is None:
                return None

            estm_result = self.estimate_widgets(is_logon_btn, screen_img_color, key_list, widgets)
            if len(estm_result) == 0:
                eng_ocr_detect_failure = True
                continue
            else:
                break

        '''如果登录候选框有多个，则选择最靠近编辑框下面的一个
        在主调用函数处处理异常！'''

        # assert len(estm_result) == 1
        if len(estm_result) != 1:
            return None

        # print "ocr detect:", estm_result[0].get('bounds')
        logging.info("ocr detect: %s", estm_result[0].get('bounds'))
        return estm_result[0]

    def ocr_detect_logon_button(self, is_logon_btn, edit_widget, shot_img_url, key_list, widgets):
        is_chinese_sim = False
        eng_ocr_detect_failure = False

        edit_coord = edit_widget.get('bounds')

        edit_coord_list = self.coord_transform(edit_coord)
        edit_left_top = edit_coord_list[0].split(',')
        edit_right_down = edit_coord_list[1].split(',')

        edit_left = int(edit_left_top[0])
        edit_upper = int(edit_left_top[1])
        edit_right = int(edit_right_down[0])
        edit_down = int(edit_right_down[1])

        for i in range(0, 2):
            if eng_ocr_detect_failure:
                is_chinese_sim = True
            self.set_language(is_chinese_sim)
            screen_img_color, height, width = self.read_screen_img(shot_img_url)
            if screen_img_color is None:
                return None

            estm_result = self.estimate_widgets(is_logon_btn, screen_img_color, key_list, widgets)
            if len(estm_result) == 0:
                eng_ocr_detect_failure = True
                continue
            else:
                break

        '''如果登录候选框有多个，则选择最靠近编辑框下面的一个
        在主调用函数处处理异常！'''

        if len(estm_result) == 0:
            return None
        elif len(estm_result) == 1:
            logging.info("ocr detect: %s", estm_result[0].get('bounds'))
            return estm_result[0]
        elif len(estm_result) > 1:
            opt_widget = estm_result[0]
            opt_coord = opt_widget.get('bounds')
            opt_coord_list = self.coord_transform(opt_coord)
            opt_left_top = opt_coord_list[0].split(',')
            opt_right_down = opt_coord_list[1].split(',')

            opt_left = int(opt_left_top[0]);    opt_upper = int(opt_left_top[1])
            opt_right = int(opt_right_down[0]); opt_down = int(opt_right_down[1])

            for n in estm_result:
                coord = n.get('bounds')
                coord_list = self.coord_transform(coord)
                left_top = coord_list[0].split(',')
                right_down = coord_list[1].split(',')

                left = int(left_top[0]);    upper = int(left_top[1])
                right = int(right_down[0]); down = int(right_down[1])

                if (opt_down > down):
                    opt_widget = n
                else:
                    continue

            # print "ocr detect:", estm_result[0].get('bounds')
            logging.info("ocr detect: %s", opt_widget.get('bounds'))
            return opt_widget

    def ocr_detect_match(self, is_logon_btn, screen_color, widget_coord, key_list):
        ''' 
        detect & match:
         1. 图像裁剪
         2. ocr检测
         3. 字符比对
        '''

        coord_list = self.coord_transform(widget_coord)
        left_top = coord_list[0].split(',')
        right_down = coord_list[1].split(',')

        left = int(left_top[0])
        upper = int(left_top[1])
        right = int(right_down[0])
        down = int(right_down[1])

        if abs(left - right) < 10 or abs(upper - down) < 10:
            return False

        self.show_img(screen_color, widget_coord)

        rc, cropped_color = self.crop(screen_color, widget_coord)
        if not rc:
            return False
        screen_width = screen_color.shape[1]
        result = self.process_and_detect(is_logon_btn, cropped_color, screen_width)

        # if os.path.exists(self.binary_file_name):
        #     os.remove(self.binary_file_name)

        if not helper.check_ocr_detect_result(is_logon_btn, key_list, result):
            return False
        else:
            return True

