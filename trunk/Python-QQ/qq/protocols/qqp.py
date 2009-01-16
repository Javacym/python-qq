# -*- coding: cp936 -*-

"""
���γ�����Դ��compass������Ե������˽���ࣺ
http://wiki.woodpecker.org.cn/moin/Compass
ԭ����:HD<mailto:hdcola@gmail.com>
�޸ģ�÷����
"""

from qq.protocols import byteprotocol
from qq.message import qqmsg
from twisted.internet import reactor

class qqProtocol(byteprotocol.ByteMessageProtocol):
    """ȱʡqqЭ��ʵ��"""
    def MessageReceived(self,packet):
        """���յ�һ����Ϣ���Ը���Ϣ���д���"""
        message = qqmsg.qqMessage()
        message.loadMessage(packet)
        # print message
        self.MessageProcess(message)

    def MessageProcess(self, message):
        """����ָ���ķ����������յ�����Ϣ"""
        method = getattr(self , "on_%s" % message.msgname, None)
        return method(message)

class qqClientQueueProtocol(qqProtocol):
    """ʹ�û������ڶ��е�qqЭ��ͻ���ʵ��"""

    def MessageReceived(self,packet):
        """���յ�һ����Ϣ��ȷ������Ϣ�Ƿ����ѷ��ͳ�����Ϣ��
        ����ǣ��ӷ�����Ϣ�������������Ϣ��Ȼ������������ִ����ȥ��
        """
        message = qqmsg.inqqMessage(self.qq)
        message.loadMessage(packet)
        # print message
        # ����������Ϣ�Ӷ��������,��û�����ѷ����б��У�����뵽�����б���
        try:
            self.sendMsg.remove(message.head.sequence)
        except ValueError:
            self.recvMsg.append(int(message.head.sequence))
            
        self.MessageProcess(message)

    def connectionMade(self):
        """���ӳɹ��ˣ��Ϳ������������߳���"""
        reactor.callInThread(self.sendQueueMesg)

    def sendDataToQueue(self, message):
        """����Ϣ��������Ͷ���"""
        if(not self.sendQueue.full()):
            self.sendQueue.put(message)
        else:
            self.call = reactor.callLater(0, self.sendDataToQueue, message)

    def sendQueueMesg(self):
        """�������е���Ϣ���ͳ�ȥ"""
        if (len(self.sendMsg) < self.WINMAX):
            while (not self.sendQueue.empty()):
                message = self.sendQueue.get()
		#���ж��Ƿ��ǽ��յ�����ˮ��
                try:
                    self.recvMsg.remove(message.head.sequence)
                except ValueError:
                    # ����ǰ������Ϣ��˳���
                    message.head.sequence = self.sequence
                    # ���Ѿ����͵���Ϣ�����Ѿ����͵��嵥��
                    self.sendMsg.append(self.sequence)
		self.sendData(message.packed())
                self.sequence += 1
		#�ж���ˮ���Ƿ����0xffffffff,����������
		if self.sequence >= 0xffff:
		    self.sequence = 0
                
        self.call = reactor.callLater(0.0001, self.sendQueueMesg)
