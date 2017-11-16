import logging

import actorcore.ICC

class OurActor(actorcore.ICC.ICC):
    def __init__(self, name, productName=None, configFile=None, logLevel=logging.INFO):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #
        actorcore.ICC.ICC.__init__(self, name,
                                   productName=productName,
                                   configFile=configFile)
        self.logger.setLevel(logLevel)
        self.everConnected = False

    def connectionMade(self):
        if self.everConnected is False:
            logging.info("alive!!!!")
            self.everConnected = True

    def disconnectActor(self):
        self.shuttingDown = True



def connectActor():
    theActor = OurActor('spsclient',
                        productName='spsClient',
                        logLevel=logging.DEBUG)
    theActor.run(doReactor=False)
    return theActor
