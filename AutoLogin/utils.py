import urllib2
import logger
import json
import traceback

def download_file(url_remote, file_name_local):
    try:
        url = url_remote.strip()

        r = urllib2.Request(url)
        req = urllib2.urlopen(r)

        save_file = open(file_name_local, 'wb')
        save_file.write(req.read())

        save_file.close()
        req.close()
        return True
    except:
        logger.logging.critical(traceback.format_exc())
        return False


# def json_parser(json_dict, key):
#     assert json_dict is not None, logger.logging.critical("Json dict is EMPTY!!!")
#     if json_dict[""]