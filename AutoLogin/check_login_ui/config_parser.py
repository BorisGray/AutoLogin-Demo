# coding: utf-8
# import ConfigParser
#
# CONFIG_DATA_PATH = './config_data/config.conf'
#
# cp = ConfigParser.SafeConfigParser()
# l = cp.read(CONFIG_DATA_PATH)
# assert len(l) != 0, "List is empty!!!"
#
# login_keys = cp.get('login', 'text_attr')
# login_keys = str(login_keys)
# login_keys = login_keys.split(',')
#
# user_keys = cp.get('user_account', 'text_attr')
# user_keys = str(user_keys)
# user_keys = user_keys.split(',')
#
# match_txt = "快速登录"
# if isinstance(match_txt, unicode):
#     match_txt = match_txt.encode('utf-8')
# # print type(match_txt)
# for key in login_keys:
#     # print type(key)
#     keys = key.strip(' ')
#     print match_txt, key
#     if key in match_txt:
#         print '该弹窗中找到的关键字为key'
#
# print '未找到'