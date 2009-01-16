# -*- coding: cp936 -*-

"""
���γ�����Դ��compass������Ե������˽���ࣺ
http://wiki.woodpecker.org.cn/moin/Compass
ԭ����:HD<mailto:hdcola@gmail.com>
�޸ģ�÷����
"""

import struct
import tea
import basic
from binascii import b2a_hex, a2b_hex

class ByteMessage:
    """��������Ϣ����"""
    
    def __init__(self):
        """��ʼ��һ����Ϣ"""
        # ��Ϣͷ
        # self.head = None
        # ��Ϣ��
        # self.body = None
	# ��Ϣβ
	# self.end  = None
        # ��Ϣ����
        # self.msgutilcls = None
        # ��ǰ����Ϣ����
        # self.msgname = ''
        # ��ǰЭ�������
        # self.protocolname = ''

    def loadMessage(self, packet):
        """�Ӷ��������м��س���Ϣ����"""
        # ���ذ�ͷ
        self.head.loadHead(packet[:len(self.head)])
        self.msgname = basic.commandinfo[self.head.id]
        # ������ϢID���ذ���
        self.body.loadBody(self.msgname, packet[len(self.head):-1])
	self.end.loadEnd(packet[-1:])

    def setMsgName(self, msgname):
        """������Ϣ��"""
        self.head.setId(basic.nametoid[msgname])
        self.msgname = msgname

    def packed(self):
        """�����ϢΪ��������PDU"""
        body = self.body.packed()
        if (body == None):
            return self.head.packed()
        else:
            self.head.setLength(len(self.head) + len(body))
            return self.head.packed() + body + self.end.packed()

    def __str__(self):
        """�ַ�����"""
        return str(self.head) + '\n' + str(self.body)+ '\n' + str(self.end)

class inByteMessageHead:
    """��������Ϣ����Ϣͷ������"""
    def __init__(self, parent):
        # ͷ
        self.packhead = basic.QQ_02_head
	# �汾
	self.ver = basic.QQ_ver
        # ����ID
        self.id = 0
        # ���к�
        self.sequence = 0
        # ����
        self.parent = parent

    def __len__(self):
        """��ͷ����7"""
        return basic.QQ_02_in_head_len

    def setId(self,id):
        """��������ID"""
        self.id = id

    def setSequence(self,sequence):
        """���÷�������"""
        self.sequence = sequence

    def setLength(self, length):
        """��������"""
        self.length = length

    def loadHead(self, header):
        """ת��һ��PDU (protocol data unit)��һ����Ϣͷ
        ��Ϣͷ�ĸ�ʽΪ��ͷ(1�ֽ�)���汾��2�ֽڣ�������ID��2�ֽڣ�����ˮ�ţ�2�ֽڣ�����7�ֽڳ���
        """
        self.packhead,self.ver,self.id,self.sequence = struct.unpack('>BHHH', header)
    
    def packed(self):
        """ת��һ����ϢͷΪ��������
        ��Ϣͷ�ĸ�ʽΪ��ͷ(1�ֽ�)���汾��2�ֽڣ�������ID��2�ֽڣ�����ˮ�ţ�2�ֽڣ�����7�ֽڳ���
        """
        return struct.pack('>BHHH', self.packhead, self.ver,self.id, self.sequence)
    def __str__(self):
        """�ַ�����"""
        plist = []
        plist.append("��ͷ:%s" % self.packhead)
	plist.append("�汾:%s" % self.ver)
        plist.append("����ID��%s" % self.id)
        plist.append("��Ϣ���кţ�%s" % self.sequence)
        return reduce(lambda x,y: x + "\n" + y, plist)

class outByteMessageHead:
    """��������Ϣ����Ϣͷ������"""
    def __init__(self, parent, qq):
        # ͷ
        self.packhead = basic.QQ_02_head
	# �汾
	self.ver = basic.QQ_ver
        # ����ID
        self.id = 0
        # ���к�
        self.sequence = 0
        # QQ����
        self.qq_id = 0
        # ����
        self.parent = parent
        #�̳�QQ�û���Ϣ
        self.qq=qq

    def __len__(self):
        """��ͷ����7"""
        return basic.QQ_02_out_head_len

    def setId(self,id):
        """��������ID"""
        self.id = id

    def setSequence(self,sequence):
        """���÷�������"""
        self.sequence = sequence

    def setLength(self, length):
        """��������"""
        self.length = length

    def loadHead(self, header):
        """ת��һ��PDU (protocol data unit)��һ����Ϣͷ
        ��Ϣͷ�ĸ�ʽΪ��ͷ(1�ֽ�)���汾��2�ֽڣ�������ID��2�ֽڣ�����ˮ�ţ�2�ֽڣ����û�QQ���룬��11�ֽڳ���
        """
        self.packhead,self.ver,self.id,self.sequence,self.qq_id = struct.unpack('>BHHHI', header)
    
    def packed(self):
        """ת��һ����ϢͷΪ��������
        ��Ϣͷ�ĸ�ʽΪ��ͷ(1�ֽ�)���汾��2�ֽڣ�������ID��2�ֽڣ�����ˮ�ţ�2�ֽڣ����û�QQ���룬��11�ֽڳ���
        """
        return struct.pack('>BHHHI', self.packhead, self.ver,self.id, self.sequence, self.qq.id)
    
    def __str__(self):
        """�ַ�����"""
        plist = []
        plist.append("��ͷ:%s" % self.packhead)
	plist.append("�汾:%s" % self.ver)
        plist.append("����ID��%s" % self.id)
        plist.append("��Ϣ���кţ�%s" % self.sequence)
        plist.append("�û�QQ��:%s" % self.qq_id)
        return reduce(lambda x,y: x + "\n" + y, plist)

class ByteMessageBody:
    """�����Ʊ��ĵ���Ϣ�������"""
    def __init__(self, parent,qq):
        # ��Ϣ������
        self.fields = {}
        self.setField = self.fields.__setitem__
        # ����
        self.parent = parent
	#ʹ��qq�û���Ϣ
	self.qq=qq

    def loadBody(self, msgname, packet):
        """ת��һ����������Ϊ��Ϣ��"""
        # �ҵ�����ķ���
        method = getattr(self.parent , "unpack_%s" %(msgname), None)
        #�����������ư��⣬�������а�����
        if msgname!='qq_pre_login':
            msg=tea.decrypt(packet,self.qq.session)
            if msg == None:
                msg=tea.decrypt(packet,self.qq.md5pwd)
                if msg == None:
                    msg=tea.decrypt(packet,self.qq.initkey)
            packet=msg
        method(packet)
        self.conversionString()
    
    def packed(self):
        """ת����Ϣ��Ϊ��������"""
        # �ҵ��������
        method = getattr(self.parent , "pack_%s" %(self.parent.msgname), None)
        send_msg = method(self.fields)
        if self.parent.msgname == 'qq_pre_login':
            return send_msg
        if self.parent.msgname == 'qq_login':
            return send_msg[:16]+tea.encrypt(send_msg[16:],self.qq.initkey)
        return tea.encrypt(send_msg,self.qq.session)

    def conversionString(self):
        """ȥ��fileds���ַ����е�\x00"""
        for field in self.fields.keys():
            if ( isinstance(self.fields[field],str) ):
                index = self.fields[field].find('\0')
                if index > -1:
                    self.fields[field] = self.fields[field][:index]

    def __str__(self):
        """�ַ�����"""
        if len(self.fields) > 0:
            plist = []
            for field in self.fields.keys():
                plist.append(str(field) + "��"  + str(self.fields[field]))
            return reduce(lambda x,y: x + "\n" + y, plist)
        else:
            return ""

    def __len__(self):
        """��Ϣ�峤��"""
        if len(self.fields) > 0:
            fields_len = 0
            for field in self.fields.keys():
                fields_len += len(str(self.fields[field]))
            return fields_len
        

class ByteMessageEnd:
    """�����Ʊ��ĵ���Ϣβ������"""
    def __init__(self, parent):
        # ��β
        self.end = 3
    def packed(self):
        """ת��һ����ϢβΪ��������"""
        return struct.pack('>B',self.end)
    def loadEnd(self,end):
	"""ת��һ����Ϣβ"""
        self.end = struct.unpack('>B', end)
