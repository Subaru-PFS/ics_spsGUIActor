import logging

import actorcore.ICC


class OurActor(actorcore.ICC.ICC):
    def __init__(self, name, productName=None, modelNames=None, configFile=None, logLevel=logging.INFO):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #
        modelNames = [] if modelNames is None else modelNames
        actorcore.ICC.ICC.__init__(self, name,
                                   productName=productName,
                                   configFile=configFile,
                                   modelNames=modelNames)

        self.logger.setLevel(logLevel)
        self.everConnected = False

    def connectionMade(self):
        if self.everConnected is False:
            logging.info("alive!!!!")
            self.everConnected = True

    def disconnectActor(self):
        self.shuttingDown = True


def connectActor(modelNames):
    theActor = OurActor('spsclient',
                        productName='spsClient',
                        modelNames=modelNames,
                        logLevel=logging.DEBUG)

    theActor.run(doReactor=False)
    return theActor
