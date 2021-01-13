# coding=utf-8
# 输出调试日志
import datetime


def debug_log(content):
    with open('./debug/' + datetime.datetime.now().strftime('%Y%m%d%H') + '.log', 'a') as f:
        f.write('\n' + str(content))
