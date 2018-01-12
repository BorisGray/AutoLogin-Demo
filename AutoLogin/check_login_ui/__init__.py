# coding:utf-8

import logging
import check_login_ui

try:
    import tornado
    import cv2
    import pytesseract
    from xml.dom import minidom
    import ConfigParser
    import urllib2
    import numpy as np

except ImportError:
    print "xxxxxxxxxxx Import module FAILURE!!! xxxxxxxxxxxxxxxxxx"


def main(j_dict):
    return check_login_ui.main_entry(j_dict)


