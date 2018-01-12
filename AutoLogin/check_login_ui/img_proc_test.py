from scipy.signal import wiener
import numpy as np
import image_processor as img_proc
import cv2
import ocr_detector
import matplotlib.pyplot as plt
import uuid
import shutil
import os
import matplotlib.animation as animation


def enhance_image(input_image):
    my_im = input_image.copy()
    my_im = wiener(my_im)
    return my_im

img = cv2.imread("../10.jpg", cv2.IMREAD_COLOR)
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('gray', img_grey)
cv2.waitKey(100)

#
# #
# # # enhanced_im=enhance_image(img_grey)
# # # cv2.imshow('Enhanced',enhanced_im)
# # # enhanced_im  = numpy.array(enhanced_im, numpy.uint8)
# # #
# # # fa = 156
# # # fb = 255
# # # # enhanced = cv2.CreateImage(cv2.GetSize(img_grey), img_grey.depth, 1)
# # # enhanced = np.zeros(img_grey.shape, np.uint8)
# # # k = 255 / (float)(fb - fa)
# # # for i in range(img_grey.shape[0]):
# # #     for j in range(img_grey.shape[1]):
# # #         if (img_grey[i][j] < fa):
# # #             enhanced[i][j] = 0
# # #         elif (img_grey[i][j] > fb):
# # #             enhanced[i][j] = 255
# # #         else:
# # #             enhanced[i][j] = k * (img_grey[i][j] - fa)
# # # cv2.imshow('enhanced', enhanced)
# # # cv2.waitKey(0)
# #
#
# # edged = cv2.Canny(img_grey, 10, 250)
# # cv2.imshow("Edged", edged)
# # cv2.waitKey(0)
# #
# #
# # #
# # _, contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # total = 0
# #
# # diff_img_color = None
# # for c in contours:
# #     # approximate the contour
# #     area = cv2.contourArea(c)
# #     # if area < 100:
# #     #     continue
# #
# #     peri = cv2.arcLength(c, True)
# #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
# #
# #     x, y, w, h = cv2.boundingRect(c)
# #     diff_img_color = cv2.rectangle(edged, (x, y), (x + w, y + h), (0, 255, 255), 2)
# #
# #     cv2.drawContours(diff_img_color, [approx], -1, (0, 255, 0), 4)
# #
# #     total += 1
# #
# # cv2.imshow("Output", diff_img_color)
# # cv2.waitKey(0)
#

# sobel = cv2.Sobel(img_grey, cv2.CV_8U, )

img_proc = img_proc.ImageProcessor(True)
cropped = img_proc.crop_logon_btn_img(img_grey)

ret, binary = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('binary', binary)
cv2.waitKey(100)




# is_most_black = img_proc.binary_most_black_pixels(binary)
# dict_col_pixels, dict_row_pixels = img_proc.count_pixels(binary, is_most_black)
#
# # fig = plt.figure()
# # axes1 = fig.add_subplot(111)
# # line, = axes1.plot(np.random.rand(10))
#
# ITER_NUM = 10
# iter = 0
# while iter < ITER_NUM:
#   smoothed_x = img_proc.smooth_curve2(dict_col_pixels, len(dict_col_pixels))
#   plt.plot(smoothed_x)
#   plt.title(iter)
#   plt.show()
#   iter = iter +1
#
# smoothed_y = img_proc.smooth_curve2(dict_row_pixels, len(dict_row_pixels))
# # plt.plot(smoothed_y)
# # plt.show()
#
# plt.subplot(221), plt.plot(smoothed_x)
# plt.subplot(223), plt.imshow(binary, 'binary')
# plt.subplot(224), plt.plot(smoothed_y)
# plt.xlabel('X & Y Axis')
# plt.ylabel('Pixel Numbers')
#
# fig_file_name = str(uuid.uuid4()) + ".jpg"
# plt.savefig('../'+fig_file_name)
# plt.show()


# shutil.copyfile(oldname,newname)
#
# # binary2 = cv2.reduce(img_grey, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
# #
# # minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(binary2)
# # print  "min val : " , minVal, " minLoc:" , minLoc
# # print  "max val : ", maxVal, " maxLoc:", maxLoc
#
#
binary_file_name = str(uuid.uuid4()) + ".jpg"
cv2.imwrite(binary_file_name, binary)

tess_ocr = ocr_detector.OcrDetector(True)
print tess_ocr.detect(binary_file_name)
#
# if os.path.exists(binary_file_name):
#     os.remove(binary_file_name)



###############################################################################################
# # -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# def data_gen():
#   t = data_gen.t
#   cnt = 0
#   while cnt < 1000:
#     cnt+=1
#     t += 0.05
#     yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
# data_gen.t = 0
#
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)
# ax.set_ylim(-1.1, 1.1)
# ax.set_xlim(0, 5)
# ax.grid()
# xdata, ydata = [], []
#
# def run(data):
#   # update the data
#   t,y = data
#   xdata.append(t)
#   ydata.append(y)
#   xmin, xmax = ax.get_xlim()
#   if t >= xmax:
#     ax.set_xlim(xmin, 2*xmax)
#     ax.figure.canvas.draw()
#   line.set_data(xdata, ydata)
#   return line,
#
# ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
#   repeat=False)
# plt.show()

# -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# fig = plt.figure()
# axes1 = fig.add_subplot(111)
# line, = axes1.plot(np.random.rand(10))
#
# def update(data):
#   line.set_ydata(data)
#   return line,
#
# def data_gen():
#   while True:
#     yield np.random.rand(10)
#
# ani = animation.FuncAnimation(fig, update, data_gen, interval=2*1000)
# plt.show()


# -*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as an

# def data_gen():
#   t = data_gen.t
#   cnt = 0
#   while cnt < 1000:
#     cnt+=1
#     t += 0.05
#     yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
# data_gen.t = 0
#
# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)
# ax.set_ylim(-1.1, 1.1)
# ax.set_xlim(0, 5)
# ax.grid()
# xdata, ydata = [], []
#
# def run(data):
#   # update the data
#   t,y = data
#   xdata.append(t)
#   ydata.append(y)
#   xmin, xmax = ax.get_xlim()
#   if t >= xmax:
#     ax.set_xlim(xmin, 2*xmax)
#     ax.figure.canvas.draw()
#   line.set_data(xdata, ydata)
#   return line,
#
# ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
#   repeat=False)
# plt.show()

# """
# ================
# The Bayes update
# ================
#
# This animation displays the posterior estimate updates as it is refitted when
# new data arrives.
# The vertical line represents the theoretical value to which the plotted
# distribution should converge.
# """
#
# # update a distribution based on new data.
# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.stats as ss
# from matplotlib.animation import FuncAnimation
#
#
# class UpdateDist(object):
#     def __init__(self, ax, prob=0.5):
#         self.success = 0
#         self.prob = prob
#         self.line, = ax.plot([], [], 'k-')
#         self.x = np.linspace(0, 1, 200)
#         self.ax = ax
#
#         # Set up plot parameters
#         self.ax.set_xlim(0, 1)
#         self.ax.set_ylim(0, 15)
#         self.ax.grid(True)
#
#         # This vertical line represents the theoretical value, to
#         # which the plotted distribution should converge.
#         self.ax.axvline(prob, linestyle='--', color='black')
#
#     def init(self):
#         self.success = 0
#         self.line.set_data([], [])
#         return self.line,
#
#     def __call__(self, i):
#         # This way the plot can continuously run and we just keep
#         # watching new realizations of the process
#         if i == 0:
#             return self.init()
#
#         # Choose success based on exceed a threshold with a uniform pick
#         if np.random.rand(1,) < self.prob:
#             self.success += 1
#         y = ss.beta.pdf(self.x, self.success + 1, (i - self.success) + 1)
#         self.line.set_data(self.x, y)
#         return self.line,
#
# fig, ax = plt.subplots()
# ud = UpdateDist(ax, prob=0.7)
# anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
#                      interval=100, blit=True)
# plt.show()


# """
# ==================
# Animated histogram
# ==================
#
# This example shows how to use a path patch to draw a bunch of
# rectangles for an animated histogram.
#
# """
# import numpy as np
#
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import matplotlib.path as path
# import matplotlib.animation as animation
#
# fig, ax = plt.subplots()
#
# # histogram our data with numpy
# data = np.random.randn(1000)
# n, bins = np.histogram(data, 100)
#
# # get the corners of the rectangles for the histogram
# left = np.array(bins[:-1])
# right = np.array(bins[1:])
# bottom = np.zeros(len(left))
# top = bottom + n
# nrects = len(left)
#
# # here comes the tricky part -- we have to set up the vertex and path
# # codes arrays using moveto, lineto and closepoly
#
# # for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# # CLOSEPOLY; the vert for the closepoly is ignored but we still need
# # it to keep the codes aligned with the vertices
# nverts = nrects*(1 + 3 + 1)
# verts = np.zeros((nverts, 2))
# codes = np.ones(nverts, int) * path.Path.LINETO
# codes[0::5] = path.Path.MOVETO
# codes[4::5] = path.Path.CLOSEPOLY
# verts[0::5, 0] = left
# verts[0::5, 1] = bottom
# verts[1::5, 0] = left
# verts[1::5, 1] = top
# verts[2::5, 0] = right
# verts[2::5, 1] = top
# verts[3::5, 0] = right
# verts[3::5, 1] = bottom
#
# barpath = path.Path(verts, codes)
# patch = patches.PathPatch(
#     barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
# ax.add_patch(patch)
#
# ax.set_xlim(left[0], right[-1])
# ax.set_ylim(bottom.min(), top.max())
#
#
# def animate(i):
#     # simulate new data coming in
#     data = np.random.randn(1000)
#     n, bins = np.histogram(data, 100)
#     top = bottom + n
#     verts[1::5, 1] = top
#     verts[2::5, 1] = top
#     return [patch, ]
#
# ani = animation.FuncAnimation(fig, animate, 100, repeat=False, blit=True)
# plt.show()


# """
# =========================
# Simple animation examples
# =========================
#
# This example contains two animations. The first is a random walk plot. The
# second is an image animation.
# """
#
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
#
# def update_line(num, data, line):
#     line.set_data(data[..., :num])
#     return line,
#
# fig1 = plt.figure()
#
# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#                                    interval=50, blit=True)
#
# # To save the animation, use the command: line_ani.save('lines.mp4')
#
# fig2 = plt.figure()
#
# x = np.arange(-9, 10)
# y = np.arange(-9, 10).reshape(-1, 1)
# base = np.hypot(x, y)
# ims = []
# for add in np.arange(15):
#     ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))
#
# im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
#                                    blit=True)
# # To save this second animation with some metadata, use the following command:
# # im_ani.save('im.mp4', metadata={'artist':'Guido'})
#
# plt.show()