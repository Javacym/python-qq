# -*- coding: cp936 -*-

"""Python-QQ�����ú���
���ߣ�÷����
ʱ�䣺2005-7-13
"""


from random import randint as _randint

#����QQ����Ҫ�ĳ�ʼ����Կ�����ڵ�½����
def initkey():
    i=0
    fills=''
    while i < 16:
        fills = fills + chr(_randint(0, 0xff))
        i += 1
    return fills

#��ΪQQ���ص�ip��ַ�ǰ������ֱ�ʾ�ģ�������Ҫת���������ǽ�����ת��Ϊip�ַ����ˡ�
#����������غ�����dejava�ṩ,QQ:18505105
def ip2string( ip ):
    a = (ip & 0xff000000) >> 24
    b = (ip & 0x00ff0000) >> 16
    c = (ip & 0x0000ff00) >> 8
    d = ip & 0x000000ff
    return "%d.%d.%d.%d" % (a,b,c,d)

#�����ǽ�ip�ַ���ת��Ϊ�����ˡ�
def string2ip( str ):
    ss = string.split(str,'.')
    ip = 0L
    for s in ss:
        ip = (ip << 8) + string.atoi(s)
    return ip

def getCommandinfo():
    """��ȡ������Ϣ"""
    return self.commandinfo

def getCommandName(commandid):
    """���ݶ����ƴ����ȡ����"""
    return commandinfo[commandid]

def getCommandName(sname):
    """���������ȡ�����ƴ���"""
    return nametoid[name]
