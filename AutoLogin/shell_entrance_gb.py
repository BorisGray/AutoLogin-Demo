# coding:utf-8 
import check_login_ui as cl 
import sys 
import os 
import cv2 
import uuid 
import csv 
import time 
import shutil 
 
work_dir = os.path.abspath('.') 
 
json_dict = {} 
json_dict['ai_module_name']  = "auto_login" 
OUT_PATH = work_dir + '/test_result/' 
FILE_PATH = work_dir + '/test_xml_img2/' 
FILE_DATA_ERROR = OUT_PATH + '/file_data_error/' 
IS_NOT_LOGIN_UI = OUT_PATH + '/is_not_login_ui/' 
IS_LOGIN_UI = OUT_PATH + '/is_login_ui/' 
 
def copy_file(json_dict, dst_path): 
    img_file = json_dict['screen_shot_url'] 
    xml_file = json_dict['dom_tree_url'] 
    if os.path.exists(img_file): 
        shutil.copy(img_file, dst_path) 
        shutil.copy(xml_file, dst_path) 
 
def call_check_login_ui(result_file_name, json_dict): 
    img = cv2.imread(json_dict['screen_shot_url'], cv2.IMREAD_COLOR) 
    result = cl.main(json_dict) 
    result_img = '' 
 
    if result is None: 
        print 'None' 
        copy_file(json_dict, IS_NOT_LOGIN_UI) 
    elif len(result) == 1: 
        print result[0] 
        copy_file(json_dict, FILE_DATA_ERROR) 
    else: 
        num_result = len(result)
        if num_result != 3:
            return None

        act = result['account']
        pwd = result['password']
        btn = result['button']

        account_x1 = account_y1 = account_x2 = account_y2 = None
        pwd_x1 = pwd_y1 = pwd_x2 = pwd_y2 = None
        btn_x1 = btn_y1 = btn_x2 = btn_y2 = None

        if act is not None:
            account_x1, account_y1 = act[0].split(',')
            account_x2, account_y2 = act[1].split(',')
            account_x1 = int(str(account_x1))
            account_y1 = int(str(account_y1))
            account_x2 = int(str(account_x2))
            account_y2 = int(str(account_y2))
            cv2.rectangle(img, (account_x1, account_y1), (account_x2, account_y2), (0, 0, 255), 2, 8)

        if pwd is not None:
            pwd_x1, pwd_y1 = pwd[0].split(',')
            pwd_x2, pwd_y2 = pwd[1].split(',')
            pwd_x1 = int(str(pwd_x1))
            pwd_y1 = int(str(pwd_y1))
            pwd_x2 = int(str(pwd_x2))
            pwd_y2 = int(str(pwd_y2))
            cv2.rectangle(img, (pwd_x1, pwd_y1), (pwd_x2, pwd_y2), (255, 0, 0), 2, 8)

        if btn is not None:
            btn_x1, btn_y1 = btn[0].split(',')
            btn_x2, btn_y2 = btn[1].split(',')
            btn_x1 = int(str(btn_x1))
            btn_y1 = int(str(btn_y1))
            btn_x2 = int(str(btn_x2))
            btn_y2 = int(str(btn_y2))
            cv2.rectangle(img, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 255, 0), 2, 8)

        # out_img = str(uuid.uuid4()) + ".png" 
        out_img = str(result_file_name)+"_result" + ".png" 
        result_img = IS_LOGIN_UI + out_img 
        cv2.imwrite(result_img, img) 
 
        if act is not None and pwd is not None and btn is not None:
            result = 'account:%s,%s,%s,%s;password:%s,%s,%s,%s;button:%s,%s,%s,%s;action:done' % (account_x1, account_y1, account_x2, account_y2, pwd_x1, pwd_y1, pwd_x2, pwd_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        elif act is not None and pwd is None and btn is not None:
            result = 'account:%s,%s,%s,%s;button:%s,%s,%s,%s;action:next' % (account_x1, account_y1, account_x2, account_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        elif act is None and pwd is not None and btn is not None:
            result = 'password:%s,%s,%s,%s;button:%s,%s,%s,%s;action:done' % (pwd_x1, pwd_y1, pwd_x2, pwd_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        print result 
 
        copy_file(json_dict, IS_LOGIN_UI) 
    return result, result_img 
 
 
def file_extension(path): 
    return os.path.splitext(path)[1] 
 
def file_name(path): 
    return os.path.splitext(path)[0] 
 
 
if __name__ == '__main__': 
 
    # out_file = open(OUT_PATH + 'test_result.txt', 'w+') 
    if not os.path.exists(OUT_PATH): 
        os.mkdir(OUT_PATH) 
 
    csvfile = file(OUT_PATH + 'test_result.csv', 'wb') 
    writer = csv.writer(csvfile) 
    writer.writerow(['文件名', '返回值', '结果图像', '运行时间', '备注']) 
 
    if not os.path.exists(FILE_DATA_ERROR): 
        os.mkdir(FILE_DATA_ERROR) 
    if not os.path.exists(IS_NOT_LOGIN_UI): 
        os.mkdir(IS_NOT_LOGIN_UI) 
    if not os.path.exists(IS_LOGIN_UI): 
        os.mkdir(IS_LOGIN_UI) 
 
    flag_break = False 
    for parent, dirnames, filenames in os.walk(FILE_PATH): 
        if flag_break: 
            break 
 
        print "parent is:" + parent 
        # for dirname in dirnames: 
        #     print  "dirname is" + dirname 
        xm_img_file_list = [] 
        # for filename in filenames: 
        for i in range(123, 125):
 
            if i == 125:
                flag_break = True 
            print "Start evaluate ", str(i), "-----------------------------------" 
            # print "parent is:" + parent 
            # print "filename is:" + filename 
 
            # print "the full name of the file i/test_result/s:" + os.path.join(parent, filename) 
 
            # name = file_name(filename) 
            # ext = file_extension(filename) 
            # if ext == ".xml": 
            filename = str(i) 
            xml_path = os.path.join(parent, filename+'.xml') 
            json_dict['dom_tree_url'] = xml_path 
            # if ext == ".jpg" or ext == ".png": 
            img_path = os.path.join(parent, filename+'.jpg') 
            json_dict['screen_shot_url'] = img_path 
 
            start = time.time() 
 
            result, result_img = call_check_login_ui(str(i), json_dict) 
                   
            end = time.time() 
            elapse = end - start 
 
            result_str = filename + "=======>" 
            if result is not  None: 
                if len(result) == 1: 
                    result = result[0] 
                else: 
                    result_str += result 
            else: 
                result = 'None' 
                 
            flag_break = True 
            # out_file.write(result_str+'\n') 
            data = (filename, result, result_img, elapse) 
            writer.writerow(data) 
 
            print "End of evaluate ", str(i), "-----------------------------------" 
    # out_file.close() 
    csvfile.close() 
