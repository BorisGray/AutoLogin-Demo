# coding:utf-8

import os
import sys
# import ConfigParser
import re
import xml_parser as xp
import image_processor
import ocr_detector
import helper
import logging

work_dir = os.path.abspath('.')
LOGGER_PATH = "/tmp/"
DATA_PATH = "../../test-data/"
CONFIG_FILE = "./AutoLogin/config_data/config.conf"

LOGON_WIDGET_CLASS = ["android.widget.Button", "android.widget.TextView", "android.view.View"]
# LOGON_WIDGET_CLASS = ["android.widget.Button"]
LOGON_WIDGET_CLASS_SUPPLEMENT = ["android.view.View"]
LOGON_TEXT_ATTR   = ["login", "logon", "登录", "下一步", "下_步", "下一个", "nextbutton","开始使用", "signin", "安全登录", "立即登录"]
LOGON_KEY         = ["login", "logon", "登录", "下一步", "下_步", "下一个", "nextbutton","开始使用", "signin", "安全登录", "立即登录"]
LOGON_RC_ID_ATTR  = ["login", "logon"]

INPUT_WIDGET_KEY  = ["输入"]

USER_WIDGET_CLASS = ["android.widget.EditText"]
USER_TEXT_ATTR    = ["account", "帐号", "账号", "user", "username", "用户名", "mobile", "手机号", "phone", "身份证", "email", "e-mail", "邮箱", "邮件地址"]
USER_ACCOUNT_KEY  = ["account", "帐号", "账号", "user", "username", "用户名", "mobile", "手机号", "phone", "身份证", "email", "e-mail", "邮箱", "邮件地址"]
USER_RC_ID_ATTR   = ["phone", "username", "account", "phone", "mobile"]

# PWD_WIDGET_CLASS  = ["android.widget.EditText", "android.widget.TextView"]
PWD_WIDGET_CLASS  = ["android.widget.EditText"]
PWD_TEXT_ATTR     = ["password", "密码", "口令"]
PWD_KEY           = ["password", "密码", "口令"]
PWD_RC_ID_ATTR    = ["password", "pwd"]


def trace_logger():
    if not os.path.exists(LOGGER_PATH):
        os.makedirs(LOGGER_PATH)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=LOGGER_PATH + 'login.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

# def read_config_file(cfg_data_file):
#     cf = ConfigParser.ConfigParser()
#     cf.read(CONFIG_FILE)
#     return cf

# fetch_config_data('login', 'text_attr')
# fetch_config_data('login', 'resource_id_attr')
# fetch_config_data('user_account', 'text_attr')
# fetch_config_data('user_account', 'resource_id_attr')
# fetch_config_data('password', 'text_attr')
# fetch_config_data('password', 'resource_id_attr')
def fetch_config_data(cf, cfg_sec, cfg_item):

    item_val = cf.get(cfg_sec, cfg_item)
    item_val = item_val.decode("utf-8")
    item_val_lst = item_val.split(",")
    return item_val_lst


def is_chinese_character(u_str):
    cn_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    u_str = u_str.decode('utf-8')
    match = cn_pattern.search(u_str)
    if match:
        return True
    else:
        return False

def ui_is_chinease_character(xml_dom_url):
    file_object = open(xml_dom_url, 'r')
    try:
        all_the_xm_text = file_object.read()
    finally:
        file_object.close()
    # print all_the_xm_text
    if is_chinese_character(all_the_xm_text):
        # print "Chinese character"
        return True
    else:
        # print "English character"
        return False


def check_in_cfg_itm_lis(attr_val, cfg_itm_val_lst):
    attr_val = attr_val.encode("utf-8")
    attr_val = attr_val.split(' ')
    attr_val = ''.join(attr_val)

    if not attr_val.strip():
        return False
    for u_s in cfg_itm_val_lst:
        # utfs = us.encode("utf-8") # if load config data from file, is OK !!
        if (u_s in attr_val) or (u_s == attr_val):
            return True
        else:
            continue
    return False


def get_candit_widget_list(node_list, widget_list):
    candit_widget_list = []
    for n in node_list:
        if n.get("class") in widget_list:
            # print("class:", n.attributes['class'].value, "coordinate:", n.attributes['bounds'].value)
            candit_widget_list.append(n)
        else:
            continue
    # print "\n"
    return candit_widget_list

# def check_ocr_detect_result(key_list, result):
#     str_result = result.encode('utf-8')
#     str_result = str_result.replace(' ', '').replace("\n", "")
#     # print str_result
#
#     if not check_in_cfg_itm_lis(str_result, key_list):
#         return False
#     else:
#         return True


# def estimate_widgets(img_proc, screen_img_color, key_list, candidate_logon_widget_list):
#
#     # img_proc = image_processor.ImageProcessor()
#     # rc, screen_img_color = img_proc.read_screen_img(shot_img_url)
#     # if not rc:
#     #     return False
#
#     print ">>>>>>>>>>>>>>>>estimate widget"
#     widget_list = []
#     for candit in candidate_logon_widget_list:
#         coord = candit.attributes['bounds'].value
#         print coord
#
#         img_proc.show_img(screen_img_color, coord)
#
#         rc, cropped_color = img_proc.crop(screen_img_color, coord)
#         if not rc:
#             return False
#
#         result = img_proc.process_and_detect(cropped_color)
#         # print type(result), result
#         if not check_ocr_detect_result(key_list, result):
#             continue
#         else:
#             widget_list.append(candit)
#     print "estimate widget<<<<<<<<<<<<<<<"
#     return widget_list


# def verify_result(detect_logon_txt_list, detect_user_account_txt_list, detect_pwd_txt_list):
#
#     # if  len(detect_logon_txt_list) == 0 \
#     #         or len(detect_user_account_txt_list) == 0 \
#     #         or len(detect_pwd_txt_list) == 0:
#     # print "xxxxxxxxxxxxxxxxxxxx is NOT login UI!!!xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#
#     assert len(detect_logon_txt_list) == 1 \
#         and len(detect_user_account_txt_list) == 1 \
#         and len(detect_pwd_txt_list) == 1,  "Detect ERROR !!!"
#
#     # print "----------------- IS logon dialog ------------------------"
#     # print "Login button coordinate:\t\t", ''.join(detect_logon_txt_list)
#     # print "User account edit box coordinate:\t", ''.join(detect_user_account_txt_list)
#     # print "Password edit box coordinate:\t\t", ''.join(detect_pwd_txt_list)

def filter_widget_by_text(esm_widg_text, key_list):
    esm_widg_text = esm_widg_text.encode('utf-8')
    esm_widg_text = esm_widg_text.split(' ')
    esm_widg_text = ''.join(esm_widg_text)

    for n in key_list:
        if n in esm_widg_text:
            if n == esm_widg_text:
                return True
            else:
                continue
        else:
            continue
    return False

def check_result(esm_logon_widg_list, esm_usr_widg_list, esm_pwd_widg_list):
    if len(esm_logon_widg_list) ==0 or len(esm_usr_widg_list) ==0 or len(esm_pwd_widg_list) == 0:
        return None
    if len(esm_usr_widg_list) > 1 or len(esm_pwd_widg_list) > 1:
        return None

    # assert len(esm_usr_widg_list) == 1, "Estimate user account widget ERROR!!!"
    # assert len(esm_pwd_widg_list) == 1, "Estimate password widget ERROR!!!"

    final_logon_coord = final_usr_coord = final_pwd_coord = []

    esm_usr_coord = esm_usr_widg_list[0].get('bounds')
    # print "user account widget coordinate: ",  esm_usr_coord
    usr_left_top, usr_right_down = helper.coord_transform(esm_usr_coord)
    usr_down = int(usr_right_down[1])

    esm_pwd_coord = esm_pwd_widg_list[0].get('bounds')
    # print "password widget coordinate: ", esm_pwd_coord
    pwd_left_top, pwd_right_down = helper.coord_transform(esm_pwd_coord)
    pwd_down = int(pwd_right_down[1])

    final_usr_coord = list(esm_usr_coord.strip('[').strip(']').split(']['))
    final_pwd_coord = list(esm_pwd_coord.strip('[').strip(']').split(']['))

    first_logon_coord = esm_logon_widg_list[0].get('bounds')
    # print "first_logon_coord= ", first_logon_coord
    opt_logon_left_top, opt_logon_right_down = helper.coord_transform(first_logon_coord)
    opt_logon_down = int(opt_logon_right_down[1])
    opt_logon_coord = list(first_logon_coord.strip('[').strip(']').split(']['))

    for n in esm_logon_widg_list:
        esm_logon_coord = n.get('bounds')
        # print "esm_logon_coord= ", esm_logon_coord
        esm_logon_class = n.get('class')
        if esm_logon_class == 'android.widget.Button':
            opt_logon_coord = list(esm_logon_coord.strip('[').strip(']').split(']['))
            break

        esm_logon_text = n.get('text')
        if filter_widget_by_text(esm_logon_text, LOGON_KEY):
            opt_logon_coord = list(esm_logon_coord.strip('[').strip(']').split(']['))
            # print "select opt logon by text: ", esm_logon_coord

        # print "logon widget coordinate: ", esm_logon_coord
        logon_left_top, logon_right_down = helper.coord_transform(esm_logon_coord)

        logon_left = int(logon_left_top[0]);    logon_upper = int(logon_left_top[1])
        logon_right = int(logon_right_down[0]); logon_down = int(logon_right_down[1])

        if logon_down > usr_down and logon_down > pwd_down:
            if logon_down < opt_logon_down:
                opt_logon_coord = list(esm_logon_coord.strip('[').strip(']').split(']['))
                # print "select opt logon by coord:  ", esm_logon_coord
        else:
            continue

    if len(opt_logon_coord) ==0:
        return None
    final_logon_coord = opt_logon_coord
    # print "final_logon_coord= ", final_logon_coord

    return final_usr_coord, final_pwd_coord, final_logon_coord


def filter_result(detect_logon_txt_list, detect_user_account_txt_list, detect_pwd_txt_list):
    if len(detect_logon_txt_list) > 1:
        for logon_widget_list in detect_logon_txt_list:
            # print logon_widget_list
            tp_left = logon_widget_list[0]
            right_down = logon_widget_list[1]

def dom_check_login_ui(j_dict):
    xml_dom_url = j_dict['dom_tree_url']
    xml_parser = xp.XmlParser()
    xml_parser.get_xml_doc(xml_dom_url)
    node_list = xml_parser.get_node_list()
    # assert len(node_list) != 0, "Dom node list is EMPTY!!!"
    if len(node_list) ==0:
        return None

    detect_logon_txt_list = []
    detect_user_account_txt_list = []
    detect_pwd_txt_list = []

    for n in node_list:
        attr_class_val = n.get('class')
        attr_text_val = n.get('text')
        attr_rc_id_val = n.get('resource-id')

        if check_in_cfg_itm_lis(attr_class_val, LOGON_WIDGET_CLASS) \
            and (check_in_cfg_itm_lis(attr_text_val, LOGON_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
                                                                                              LOGON_RC_ID_ATTR)):
            # print("logon button: ", n.get('bounds'))
            detect_logon_txt_list.append(n)

        if check_in_cfg_itm_lis(attr_class_val, USER_WIDGET_CLASS) \
                and (check_in_cfg_itm_lis(attr_text_val, USER_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
                                                                                                 USER_RC_ID_ATTR)):
            # print("user edit box: ", n.get('bounds'))
            # detect_user_account_txt_list.append(n.get('bounds'))
            detect_user_account_txt_list.append(n)

        if check_in_cfg_itm_lis(attr_class_val, PWD_WIDGET_CLASS) \
                and (check_in_cfg_itm_lis(attr_text_val, PWD_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
                                                                                                PWD_RC_ID_ATTR)):
            # print("password edit box: ", n.get('bounds'))
            # detect_pwd_txt_list.append(n.get('bounds'))
            detect_pwd_txt_list.append(n)

    # assert len(detect_user_account_txt_list) == 1 \
    #        and len(detect_pwd_txt_list) == 1, "Detect ERROR !!!"

    return detect_user_account_txt_list, detect_pwd_txt_list, detect_logon_txt_list

def dom_estm_widget(candit_wid_list, txt_key_list, rc_id_key_list):
    estm_wid_list = []
    for n in candit_wid_list:
        # attr_class_val = n.get('class')
        attr_text_val = n.get('text')
        attr_rc_id_val = n.get('resource-id')

        if check_in_cfg_itm_lis(attr_text_val, txt_key_list) or check_in_cfg_itm_lis(attr_rc_id_val,
                                                                                     rc_id_key_list):
            # print("logon button: ", n.get('bounds'))
            estm_wid_list.append(n)
    return estm_wid_list
#
# def dom_check_login_ui(j_dict):
#     xml_dom_url = j_dict['dom_tree_url']
#     # shot_img_url = j_dict['screen_shot_url']
#
#     xml_parser = xp.XmlParser()
#     xml_parser.get_xml_doc(xml_dom_url)
#     node_list = xml_parser.get_node_list()
#     assert len(node_list) != 0, "Dom node list is EMPTY!!!"
#
#     detect_logon_txt_list = []
#     detect_user_account_txt_list = []
#     detect_pwd_txt_list = []
#
#     for n in node_list:
#         attr_class_val = n.get('class')
#         attr_text_val = n.get('text')
#         attr_rc_id_val = n.get('resource-id')
#
#         # print "class: ", attr_class_val, \
#         #     "\t text: ", attr_text_val, \
#         #     "\t resource-id:", attr_rc_id_val
#
#
#         # if check_in_cfg_itm_lis(attr_class_val, LOGON_WIDGET_CLASS) \
#         #         and (check_in_cfg_itm_lis(attr_text_val, LOGON_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
#         #                                                                                           LOGON_RC_ID_ATTR)):
#         #     print("logon button: ", n.get('bounds'))
#         #     detect_logon_txt_list.append(n.get('bounds'))
#         #
#         #
#         # if check_in_cfg_itm_lis(attr_class_val, USER_WIDGET_CLASS) \
#         #         and (check_in_cfg_itm_lis(attr_text_val, USER_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
#         #                                                                                          USER_RC_ID_ATTR)):
#         #     print("user edit box: ", n.get('bounds'))
#         #     detect_user_account_txt_list.append(n.get('bounds'))
#         #
#         #
#         # if check_in_cfg_itm_lis(attr_class_val, PWD_WIDGET_CLASS) \
#         #         and (check_in_cfg_itm_lis(attr_text_val, PWD_TEXT_ATTR) or check_in_cfg_itm_lis(attr_rc_id_val,
#         #                                                                                         PWD_RC_ID_ATTR)):
#     #         print("password edit box: ", n.get('bounds'))
#     #         detect_pwd_txt_list.append(n.get('bounds'))
#     #
#     # if len(detect_logon_txt_list) == 0 \
#     #         or len(detect_user_account_txt_list) == 0 \
#     #         or len(detect_pwd_txt_list) == 0:
#     #     print "xxxxxxxxxxxxxxxxxxxx is NOT login UI!!!xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#     #     return False
#     #
#     # filter_result(detect_logon_txt_list, detect_user_account_txt_list, detect_pwd_txt_list)
#     #
#     # assert len(detect_logon_txt_list) == 1 \
#     #        and len(detect_user_account_txt_list) == 1 \
#     #        and len(detect_pwd_txt_list) == 1, "Detect ERROR !!!"
#     #
#     # print "----------------- IS logon dialog ------------------------"
#     # print "Login button coordinate:\t\t", ''.join(detect_logon_txt_list)
#     # print "User account edit box coordinate:\t", ''.join(detect_user_account_txt_list)
#     # print "Password edit box coordinate:\t\t", ''.join(detect_pwd_txt_list)
#     # return True, detect_logon_txt_list, detect_user_account_txt_list, detect_pwd_txt_list

# def ocr_check_login_ui(j_dict):


def verify_result(estm_user_edit, estm_pwd_edit, estm_login_button):
    # assert  estm_user_edit is not None and estm_pwd_edit is not None and estm_login_button is not None
    # if estm_user_edit is None or estm_login_button is None:
    if estm_login_button is None:
        return None

    est_usr_coord = None
    if estm_user_edit is not None:
        est_usr_coord = estm_user_edit.get('bounds')

    est_pwd_coord = None
    if estm_pwd_edit is not None:
        est_pwd_coord = estm_pwd_edit.get('bounds')

    est_login_coord = estm_login_button.get('bounds')

    final_usr_coord = None
    if  estm_user_edit is not None:
        final_usr_coord = list(est_usr_coord.strip('[').strip(']').split(']['))

    final_pwd_coord = None
    if estm_pwd_edit is not None:
        final_pwd_coord = list(est_pwd_coord.strip('[').strip(']').split(']['))

    final_login_coord = list(est_login_coord.strip('[').strip(']').split(']['))

    logging.info("--------Auto Login Verification End----------------------------")
    if estm_pwd_edit is None:
        return {'account': final_usr_coord, 'password':None, 'button': final_login_coord}

    elif estm_user_edit is None:
        return {'account':None, 'password': final_pwd_coord, 'button': final_login_coord}
    else:
        return {'account': final_usr_coord, 'password': final_pwd_coord, 'button': final_login_coord}


# def ocr_detect(img_proc, shot_img_url, key_list, widgets):
#     is_chinese_sim = False
#     eng_ocr_detect_failure = False
#     for i in range(0, 2):
#         if eng_ocr_detect_failure:
#             is_chinese_sim = True
#         img_proc.set_language(is_chinese_sim)
#         screen_img_color = img_proc.read_screen_img(shot_img_url)
#         if screen_img_color is None:
#             return None
#         estm_result = img_proc.estimate_widgets(screen_img_color, key_list, widgets)
#         if estm_result is None:
#             eng_ocr_detect_failure = True
#             continue
#         else:
#             break
#     return estm_result

def main_entry(j_dict):
    trace_logger()

    xml_dom_url = j_dict['dom_tree_url']
    shot_img_url = j_dict['screen_shot_url']
    logging.info("--------Auto Login Verification Start----------------------------")
    logging.info("dom tree file:" + xml_dom_url)
    logging.info("screen shot file:" + shot_img_url)

    # ocr识别默认采用英文，分别用英文和中文字符集做2次识别
    is_chinese_sim = False
    img_proc = image_processor.ImageProcessor(is_chinese_sim)
    
    # 读入全图和XML数据,XML数据返回全部node节点数据
    screen_img_color, height, width = img_proc.read_screen_img(shot_img_url)
    if screen_img_color is None:
        return [" Read image file FAILURE!!!"]

    xml_parser = xp.XmlParser()
    node_list = xml_parser.get_xml_data(xml_dom_url)
    if node_list is None:
        return [" Read xml file FAILURE!!!"]

    ##########################################################################################
    edit_text_widgets = xml_parser.get_edit_text_widgets(node_list, USER_WIDGET_CLASS)
    '''读取xml控件类型:编辑框可能有其他类型'''

    btn_widgets = xml_parser.get_btn_widget(node_list, LOGON_WIDGET_CLASS)
    '''读取xml控件类型:登录框类型可能有其他类型'''
    for n in btn_widgets:
        logging.info("candidate logon widget1: " + str(n.get('bounds')))

    estm_login_button = None
    if len(btn_widgets) == 0:
        '''如果没有指定类型的按钮.则以android.view.View进行ocr识别'''
        btn_widgets = xml_parser.get_btn_widget(node_list, LOGON_WIDGET_CLASS_SUPPLEMENT)
        estm_login_button = img_proc.ocr_detect(True, shot_img_url, LOGON_KEY, btn_widgets)

    flag = xml_parser.is_login_ui(edit_text_widgets, btn_widgets)
    if flag:
        logging.info("current ui is logon dialog !")
    else:
        logging.info("current ui is NOT logon dialog !!!")
        return None

    estm_user_edits = xml_parser.xml_estm_edit(edit_text_widgets, USER_TEXT_ATTR, USER_RC_ID_ATTR)
    '''根据xml读取属性信息不可靠'''
    estm_user_edit = None
    is_logon_btn = False
    if len(estm_user_edits) == 0:
        estm_user_edit = img_proc.ocr_detect(is_logon_btn, shot_img_url, USER_ACCOUNT_KEY, edit_text_widgets)
    elif len(estm_user_edits) > 1:
        estm_user_edit = img_proc.ocr_detect(is_logon_btn, shot_img_url, USER_ACCOUNT_KEY, estm_user_edits)
    elif len(estm_user_edits) == 1:
        estm_user_edit = estm_user_edits[0]
    # if estm_user_edit is None:
    #     return None
    if estm_user_edit is not None:
        logging.info("FINAL detect user edit: " + str(estm_user_edit.get('bounds')))

    num_edit_text_widgets = len(edit_text_widgets)
    estm_pwd_edit = None
    if num_edit_text_widgets >= 1:
    # if num_edit_text_widgets > 1:
        estm_pwd_edits = xml_parser.xml_estm_edit(edit_text_widgets, PWD_TEXT_ATTR, PWD_RC_ID_ATTR)
        if len(estm_pwd_edits) == 0:
            estm_pwd_edit = img_proc.ocr_detect(is_logon_btn, shot_img_url, PWD_KEY, edit_text_widgets)
        elif len(estm_pwd_edits) > 1:
            estm_pwd_edit = img_proc.ocr_detect(is_logon_btn, shot_img_url, PWD_KEY, estm_pwd_edits)
        elif len(estm_pwd_edits) == 1:
            estm_pwd_edit = estm_pwd_edits[0]
        # assert estm_pwd_edit is not None
        # if estm_pwd_edit is None:
        #     return None
        if estm_pwd_edit is not None:
            logging.info("FINAL detect password edit: " + str(estm_pwd_edit.get('bounds')))


    candid_login_buttons = xml_parser.xml_estm_button(estm_user_edit, estm_pwd_edit, btn_widgets, LOGON_KEY)
    '''xml读取属性信息不可靠'''
    # assert len(candid_login_buttons) >= 1
    # if len(candid_login_buttons) == 0:
    #     return None

    for n in candid_login_buttons:
        logging.info("candidate logon widget2: " + str(n.get('bounds')))

    estm_login_buttons = None
    edit_widget = None
    if len(candid_login_buttons) == 1:
        estm_login_button = candid_login_buttons[0]
    elif len(candid_login_buttons) > 1 or len(candid_login_buttons) == 0:
        if estm_user_edit is not None and estm_pwd_edit is not None:
            edit_widget = estm_pwd_edit
        if estm_user_edit is not None and estm_pwd_edit is None:
            edit_widget = estm_user_edit
        if estm_user_edit is None and estm_pwd_edit is not None:
            edit_widget = estm_pwd_edit
        if estm_user_edit is None and estm_pwd_edit is None:
            return None
        estm_login_button = img_proc.ocr_detect_logon_button(True, edit_widget, shot_img_url, LOGON_KEY, candid_login_buttons)
    # assert estm_login_button is not None
    if estm_login_button is None:
        return None
    logging.info("FINAL detect logon button: " + str(estm_login_button.get('bounds')))

    return verify_result(estm_user_edit, estm_pwd_edit, estm_login_button)


    ##########################################################################################
    # candid_user_widget_list = xml_parser.get_widget_list(node_list, "class", USER_WIDGET_CLASS)
    #
    #
    # eng_ocr_detect_failure = False
    # ocr_esm_logon_widg_list = ocr_esm_usr_widg_list = ocr_esm_pwd_widg_list = []
    #
    # xml_estm_user = xml_parser.estm_widget(candid_user_widget_list, USER_TEXT_ATTR, USER_RC_ID_ATTR)
    # # if len(xml_estm_user) == 1:
    # #     esm_usr_widg_list = xml_estm_user
    # for n in xml_estm_user:
    #     logging.info("xml estimate user widget:" + str(n.get('bounds')))
    #
    # for i in range(0, 2):
    #     if eng_ocr_detect_failure:
    #         is_chinese_sim = True
    #
    #
    # candidate_logon_widget_list = get_candit_widget_list(node_list, LOGON_WIDGET_CLASS)
    # candidate_user_widget_list = get_candit_widget_list(node_list, USER_WIDGET_CLASS)
    # candidate_pwd_widget_list = get_candit_widget_list(node_list, PWD_WIDGET_CLASS)
    #
    # # candidate_logon_widget_list, candidate_user_widget_list, candidate_pwd_widget_list = \
    # #     get_candit_widget_list(node_list, LOGON_WIDGET_CLASS, USER_WIDGET_CLASS, PWD_WIDGET_CLASS)
    #
    #
    # for i in range(0, 2):
    #     if eng_ocr_detect_failure:
    #         is_chinese_sim = True
    #
    #     img_proc = image_processor.ImageProcessor(is_chinese_sim)
    #     rc, screen_img_color = img_proc.read_screen_img(shot_img_url)
    #     if not rc:
    #         return None
    #
    #     ocr_esm_logon_widg_list = img_proc.estimate_widgets(screen_img_color, LOGON_KEY, candidate_logon_widget_list)
    #     for n in ocr_esm_logon_widg_list:
    #         logging.info("OCR estimate logon widget: " + str(n.get('bounds')))
    #
    #     ocr_esm_usr_widg_list = img_proc.estimate_widgets(screen_img_color, USER_ACCOUNT_KEY, candidate_user_widget_list)
    #     for n in ocr_esm_usr_widg_list:
    #         logging.info("OCR estimate user widget: " + str(n.get('bounds')))
    #
    #     ocr_esm_pwd_widg_list = img_proc.estimate_widgets(screen_img_color, PWD_KEY, candidate_pwd_widget_list)
    #     for n in ocr_esm_pwd_widg_list:
    #         logging.info("OCR estimate password widget: " + str(n.get('bounds')))
    #
    #     if len(ocr_esm_logon_widg_list) == 0 or len(ocr_esm_usr_widg_list)==0 or len(ocr_esm_pwd_widg_list) == 0 :
    #         eng_ocr_detect_failure = True
    #         continue
    #     else:
    #         break
    #
    # esm_usr_widg_list = esm_pwd_widg_list = esm_logon_widg_list = []
    # user_num = len(ocr_esm_usr_widg_list)
    # pwd_num = len(ocr_esm_pwd_widg_list)
    # logon_num = len(ocr_esm_logon_widg_list)
    #
    # if user_num == 1 and pwd_num == 1:
    #     esm_usr_widg_list = ocr_esm_usr_widg_list
    #     esm_pwd_widg_list = ocr_esm_pwd_widg_list
    #
    # # Parse dom xml
    # if user_num == 0:
    #     dom_estm_user_wid = dom_estm_widget(candidate_user_widget_list, USER_TEXT_ATTR, USER_RC_ID_ATTR)
    #     if len(dom_estm_user_wid) == 1:
    #         esm_usr_widg_list = dom_estm_user_wid
    #     for n in dom_estm_user_wid:
    #         logging.info( "estimate user widget:" + str(n.get('bounds')))
    #
    # if pwd_num == 0:
    #     dom_estm_pwd_wid = dom_estm_widget(candidate_pwd_widget_list, PWD_TEXT_ATTR, PWD_RC_ID_ATTR)
    #     if len(dom_estm_pwd_wid) == 1:
    #         esm_pwd_widg_list = dom_estm_pwd_wid
    #     for n in dom_estm_pwd_wid:
    #         logging.info("estimate password widget:" + str(n.get('bounds')))
    #
    # if logon_num == 0:
    #     dom_estm_login_wid = dom_estm_widget(candidate_logon_widget_list, LOGON_TEXT_ATTR, LOGON_RC_ID_ATTR)
    #     if len(dom_estm_login_wid) == 1:
    #         esm_logon_widg_list = dom_estm_login_wid
    #     for n in dom_estm_login_wid:
    #         logging.info("estimate logon widget:" + str(n.get('bounds')))
    # elif logon_num >= 1:
    #     esm_logon_widg_list = ocr_esm_logon_widg_list
    #
    # # xml_esm_usr_widg_list, xml_esm_pwd_widg_list, xml_esm_logon_widg_list = dom_check_login_ui(j_dict)
    # # logging.info("Dom tree detect result................")
    # # for n in xml_esm_usr_widg_list:
    # #     logging.info( "estimate user widget:" + str(n.get('bounds')))
    # # for n in xml_esm_pwd_widg_list:
    # #     logging.info("estimate password widget:" + str(n.get('bounds')))
    # # for n in xml_esm_logon_widg_list:
    # #     logging.info("estimate logon widget:" + str(n.get('bounds')))
    #
    # return check_result(esm_logon_widg_list, esm_usr_widg_list, esm_pwd_widg_list)


def main_entry2(json_dict):
    trace_logger()

    xml_dom_url = json_dict['dom_tree_url']
    shot_img_url = json_dict['screen_shot_url']
    logging.info("--------Auto Login Verification Start----------------------------")
    logging.info("dom tree file:" + xml_dom_url)
    logging.info("screen shot file:" + shot_img_url)

    # ocr识别默认采用英文，分别用英文和中文字符集做2次识别
    is_chinese_sim = False
    img_proc = image_processor.ImageProcessor(is_chinese_sim)

    # 读入全图和XML数据,XML数据返回全部node节点数据
    screen_img_color, height, width = img_proc.read_screen_img(shot_img_url)
    if screen_img_color is None:
        return [" Read image file FAILURE!!!"]

    xml_parser = xp.XmlParser()
    node_list = xml_parser.get_xml_data(xml_dom_url)
    if node_list is None:
        return [" Read xml file FAILURE!!!"]

    ''' 
    判断是否是登录框的标准依据2条， 一个是关键字信息，另一个是通过ocr获取控件位置关联信息
    比如帐号编辑框， 如返回结果有多个，需要结合关键字和控件位置信息进行筛选。
    ocr的识别准确度是关键,登录按钮可能需要裁边后再做ocr
    一次遍历获得所有的候选信息，再依据位置关系进行筛选
    矩形识别判断登录按钮.
    
    针对ui是webview的特例的情况，直接调用图形检测和ocr, 当前逻辑如果根节点ocr最后没有返回正确信息，则调用图形检测和ocr模块
    '''
    # 全图矩形检测，找出登录按钮, 再进行ocr检测
    ''' 
    ocr检测帐号和密码编辑框， 不用xml的控件类型等不可靠的属性信息
    结果将控件属性值和ocr结果进行关联
    
    关键字信息采用NLP语义分析
    '''

    leaf_node_list = []
    for n in node_list:
        children_node = n.getchildren()
        if len(children_node) == 0:
            leaf_node_list.append(n)

    account_candidate = []
    pwd_candidate = []
    login_candidate = []

    for n in leaf_node_list:
        coord = n.get('bounds')
        if coord is None:
            continue

        eng_ocr_detect_failure = False
        for i in range(0, 2):
            if eng_ocr_detect_failure:
                is_chinese_sim = True
            img_proc.set_language(is_chinese_sim)

            flag_account = img_proc.ocr_detect_match(False, screen_img_color, coord, USER_ACCOUNT_KEY)
            flag_pwd = img_proc.ocr_detect_match(False, screen_img_color, coord, PWD_KEY)
            flag_login = img_proc.ocr_detect_match(True, screen_img_color, coord, LOGON_KEY)
            if not flag_account and not flag_pwd and not flag_login:
                eng_ocr_detect_failure = True
                continue
            else:
                if flag_account:
                    account_candidate.append(n)
                elif flag_pwd:
                    pwd_candidate.append(n)
                elif flag_login:
                    login_candidate.append(n)
                break

    print 'Account Candidates:'
    for n1 in account_candidate:
        print n1.get('bounds')
    print 'Password Candidates:'
    for n2 in pwd_candidate:
        print n2.get('bounds')
    print 'Login Candidates:'
    for n3 in login_candidate:
        print n3.get('bounds')

    # 全图矩形检测，找出登录按钮, 再进行ocr检测
    # process_candidates(height, width, account_candidate, nlppwd_candidate, login_candidate)


# if __name__ == '__main__':
#     print('\nUsage:')
#     print('\ncheck_login_ui.py [dom_tree_url]  [screen_shot_url]\n\n')
#
#     if len(sys.argv) < 3:
#         print(' (ERROR) You must call this script with two argument!!!\n')
#         quit()
#
#     json_dict = {}
#     json_dict['ai_module_name']  = "auto_login"
#     # json_dict['dom_tree_url']    = "/root/workspace/devicepass-ai/auto_login/check_login_ui/test_data/一点金库理财-1.3.9/HTC D10w登录.xml"
#     # json_dict['screen_shot_url'] = "/root/workspace/devicepass-ai/auto_login/check_login_ui/test_data/一点金库理财-1.3.9/HTC  D10w 登录.jpg"
#
#     json_dict['dom_tree_url']    = sys.argv[1]
#     json_dict['screen_shot_url'] = sys.argv[2]
#
#     main_entry(json_dict)
