# -*- coding: cp936 -*-

"""
���γ�����Դ��compass������Ե������˽���ࣺ
http://wiki.woodpecker.org.cn/moin/Compass
ԭ����:HD<mailto:hdcola@gmail.com>
�޸ģ�÷����
"""

from twisted.internet import protocol, defer
import struct

class ByteMessageProtocol(protocol.DatagramProtocol):
    """��������Э�鴦�������"""
    def __init__(self):
        # ������Ϣ�Ļ�����
        self.buffer = ''

    def datagramReceived(self, data,(host, port)):
        """ �鿴������PDU(protocol data unit)��
        ����Ϣ����rawMessageReceived�����д���
        """
	defer.succeed(self.MessageReceived(data))

    def sendData(self, data):
        """�����ķ��ͳ�ȥ"""
        self.transport.write(data, self.qq.server)

    def MessageReceived(self,packet):
        """���ض���������Ϣ��һ��Ҫ�̳б�����"""
        pass
