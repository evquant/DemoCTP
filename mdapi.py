# encoding: UTF-8

import os
import sys

from PyQt4 import QtGui
from time import sleep
from vnctpmd import *
from eventdriven import *
from listeners import *

class TestMdApi(MdApi):

    def __init__(self):
        super(TestMdApi, self).__init__()
        self.__reqid = 0
        self.__engine = None

    def onFrontConnected(self):
        print u'md已连接服务器'

    def onFrontDisconnected(self, n):
        print u'md服务器已断开：' + n

    def onRspError(self, error, n, last):
        state = {'n' : n, 'last' : last}
        event = Event(EVNET_MD_RSPERROR, error=error, state=state)
        self.__engine.put(event)
        #print u'错误'


    def onRspUserLogin(self, data, error, n, last):
        state = {'n' : n, 'last' : last}
        event = Event(EVENT_MD_LOGIN, data, error, state)
        self.__engine.put(event)
        #print u'用户登录'

    def onRspSubMarketData(self, data,error, n, last):
        #print u'订阅行情应答'
        #print data
        #print error
        pass

    def onRspUnSubMarketData(self, data, error, n, last):
        #print u'退订行情应答'
        #print data
        #print error
        pass

    def onRtnDepthMarketData(self, data):
        event = Event(type=EVENT_MD_DATA, data=data)
        self.__engine.put(event)
        #print u'深度行情通知'


    # 以下为主动函数
    def login(self, username, password, address, brokerid):

        self.createFtdcMdApi(os.getcwd() + '\\mdconnection\\')
        self.registerFront(address)         #self.registerFront('tcp://180.168.146.187:10010')
        self.init()
        sleep(0.5)

        loginReq = {}
        loginReq['UserID'] = username       #'020956'
        loginReq['Password'] = password     #'18936803910'
        loginReq['BrokerID'] = brokerid     #'9999'
        self.__reqid = self.__reqid + 1
        self.reqUserLogin(loginReq, self.__reqid)

    def subscribe(self, instrumentID):
        self.subscribeMarketData(instrumentID)

    def unsubscribe(self, instrumentID):
        self.unSubscribeMarketData(instrumentID)

    def registerEngine(self, engine):
        self.__engine = engine


def main():

    app = QtGui.QApplication(sys.argv)
    engine = EventDispatcher()
    engine.registerListener(EVENT_MD_LOGIN, onMdLogin)
    engine.registerListener(EVNET_MD_RSPERROR, onMdError)
    engine.registerListener(EVENT_MD_DATA, onMdData)

    md = TestMdApi()
    md.registerEngine(engine)
    md.login('020956', '18936803910', 'tcp://180.168.146.187:10010','9999')
    md.subscribe('CF509')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


