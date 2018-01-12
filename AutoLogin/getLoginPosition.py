# coding:utf-8
import devicepassai.AutoLogin.check_login_ui as cl
import sys

# print('\nUsage:')
# print('\nshell_entrance.py [dom_tree_url]  [screen_shot_url]\n\n')

if not len(sys.argv)==3:
    raise AssertionError(' (ERROR) You must call this script with two argument!!!')

xml_path = str(sys.argv[1])
img_path = str(sys.argv[2])

json_dict = {}
json_dict['ai_module_name']  = "auto_login"

json_dict['dom_tree_url']    = xml_path
json_dict['screen_shot_url'] = img_path
result = cl.main(json_dict)

console_result = None
if result is None:
    print 'None'
elif len(result) == 3:

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

        if pwd is not None:
            pwd_x1, pwd_y1 = pwd[0].split(',')
            pwd_x2, pwd_y2 = pwd[1].split(',')
            pwd_x1 = int(str(pwd_x1))
            pwd_y1 = int(str(pwd_y1))
            pwd_x2 = int(str(pwd_x2))
            pwd_y2 = int(str(pwd_y2))

        if btn is not None:
            btn_x1, btn_y1 = btn[0].split(',')
            btn_x2, btn_y2 = btn[1].split(',')
            btn_x1 = int(str(btn_x1))
            btn_y1 = int(str(btn_y1))
            btn_x2 = int(str(btn_x2))
            btn_y2 = int(str(btn_y2))

        if act is not None and pwd is not None and btn is not None:
                console_result = 'account:%s,%s,%s,%s;password:%s,%s,%s,%s;button:%s,%s,%s,%s;action:done' % (account_x1, account_y1, account_x2, account_y2, pwd_x1, pwd_y1, pwd_x2, pwd_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        elif act is not None and pwd is None and btn is not None:
                console_result = 'account:%s,%s,%s,%s;button:%s,%s,%s,%s;action:next' % (account_x1, account_y1, account_x2, account_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        elif act is None and pwd is not None and btn is not None:
                console_result = 'password:%s,%s,%s,%s;button:%s,%s,%s,%s;action:done' % (pwd_x1, pwd_y1, pwd_x2, pwd_y2, btn_x1, btn_y1, btn_x2, btn_y2)
        print console_result

