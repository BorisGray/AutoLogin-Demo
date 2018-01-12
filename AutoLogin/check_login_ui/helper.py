# coding: utf-8
import logging
def check_in_cfg_itm_list(attr_val, cfg_itm_val_lst):
    # attr_val = attr_val.encode("utf-8")
    # print "check_in_cfg_itm_list", attr_val
    if attr_val is None:
        return False

    for u_s in cfg_itm_val_lst:
        # utfs = us.encode("utf-8") # if load config data from file, is OK !!
        if (u_s in attr_val) or (u_s == attr_val):
            # print   attr_val,  " matched ", u_s
            logging.info(attr_val + " MATCHED "+ u_s)
            return True
        else:
            logging.info(attr_val + " NOT matched " + u_s)
            continue
    return False

def check_in_btn_list(attr_val, cfg_itm_val_lst):
    # attr_val = attr_val.encode("utf-8")
    # print "check_in_cfg_itm_list", attr_val
    if attr_val is None:
        return False

    for u_s in cfg_itm_val_lst:
        # utfs = us.encode("utf-8") # if load config data from file, is OK !!
        # 2017-7-28 关键字匹配放宽了条件, 匹配时会增加冗余数据
        # if u_s == attr_val or u_s in attr_val:
        if u_s == attr_val:
            logging.info(attr_val + " MATCHED " + u_s)
            return True
        else:
            logging.info(attr_val + " NOT matched " + u_s)
            continue
    return False

def check_ocr_detect_result(is_logon_btn, key_list, result):
    str_result = result.encode('utf-8')
    str_result = str_result.lower()
    str_result = str_result.replace(' ', '').replace("\n", "")
    str_result = str_result.split(' ')
    str_result = ''.join(str_result)
    # print str_result

    if is_logon_btn:
        if not check_in_btn_list(str_result, key_list):
            return False
        else:
            return True
    else:
        if not check_in_cfg_itm_list(str_result, key_list):
            return False
        else:
            return True


def coord_transform(coord):
    # print type(coord), coord
    coord = coord.strip('[').strip(']').split('][')
    coord_list = list(coord)

    left_top = coord_list[0].split(',')
    right_down = coord_list[1].split(',')

    return left_top, right_down