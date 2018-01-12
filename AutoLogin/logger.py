# coding: utf-8
import os
import logging

# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import animation
#
# fig = plt.figure()
# data = np.random.random((255, 255))
# im = plt.imshow(data, cmap='gray')
#
# # animation function.  This is called sequentially
# def animate(i):
#     data = np.random.random((255, 255))
#     im.set_array(data)
#     return [im]
#
# anim = animation.FuncAnimation(fig, animate, frames=200, interval=600, blit=True)
# plt.show()









# TEMP_PATH = "../tmp/"
# def trace_logger():
#     if not os.path.exists(TEMP_PATH):
#         os.makedirs(TEMP_PATH)
#
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filename=TEMP_PATH + 'logger.log',
#                         filemode='w')
#
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
