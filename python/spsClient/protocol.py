__author__ = 'alefur'
from twisted.internet.protocol import Protocol, ReconnectingClientFactory


class Echo(Protocol):
    def __init__(self, readCallback):
        self.readCallback = readCallback

    def dataReceived(self, data):
        self.readCallback(data)

    def sendMessage(self, msg):
        self.transport.write("%s\n" % msg)


class EchoClientFactory(ReconnectingClientFactory):
    def __init__(self, spsClient):
        self.spsClient = spsClient
        self.cmdID = 0
        self.isStarted = False

        self.readCallback = self.logMsg
        self.connectedCallback = self.isnowConnected

    def clientReady(self, client):
        self.client = client
        self.connectedCallback()

    def startedConnecting(self, connector):
        #print 'Started to connect.'
        pass

    def isnowConnected(self):
        #print "isnowConnected"
        pass

    def logMsg(self, msg):
        if not self.isStarted:
            self.doCmd("hub listen addActors *")
            self.isStarted = True

        msg = msg.split('\n')
        for m in msg:
            print m

    def doCmd(self, cmd):

        cmd = str(cmd) if type(cmd) is not str else cmd

        cmd = "%s %d %s" % (self.spsClient.cmdrName, self.cmdID, cmd)

        self.cmdID += 1
        self.send_msg(cmd)

    def buildProtocol(self, addr):
        #print 'Connected.'
        #print 'Resetting reconnection delay'
        self.resetDelay()
        self.myProto = Echo(self.readCallback)
        return self.myProto

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        pass

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason

    def send_msg(self, msg):
        self.myProto.sendMessage(msg)