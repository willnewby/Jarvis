#!/usr/bin/python
# -*- coding: koi8-r -*-
# $Id: bot.py,v 1.2 2006/10/06 12:30:42 normanr Exp $
# Based on framework at http://xmpppy.sourceforge.net/examples/bot.py
import sys
import xmpp
import commands
import logging
import os

class Jarvis:

    __LOG_LOCATION__ = "log/jarvis.log"

    def __init__(self):

        # Status indicating whether to continue
        # It's not threadsafe, but whatever
        self.status = True

        self.__setupLogger__()

        # Set up processor
        self.processor = commands.MessageProcessor(self.logger)

    def __setupLogger__(self):

        self.logger = logging.getLogger('Jarvis')
        self.logger.setLevel(logging.DEBUG)

        # Log formatting
        formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Logfile handler
        dir = os.path.dirname(self.__LOG_LOCATION__)
        if not os.path.exists(dir):
            os.makedirs(dir)

        fh = logging.FileHandler(self.__LOG_LOCATION__)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def connect(self, username, password):

        # Create the connection
        jid = xmpp.protocol.JID(username)
        user = jid.getNode()
        server = jid.getDomain()

        self.conn = xmpp.Client(server,debug=[])
        conres = self.conn.connect(("talk.google.com", 5222))

        if not conres:
            self.logger.error("Unable to connect to server %s!" % server)
            sys.exit(1)
        if conres<>'tls':
            self.logger.warn("Unable to estabilish secure connection - TLS failed!")

        authres = self.conn.auth(user, password)

        if not authres:
            self.logger.error("Unable to authorize on %s - check login/password." % server)
            sys.exit(1)
        if authres<>'sasl':
            self.logger.warn("Warning: unable to perform SASL auth os %s. Old authentication method used!" % server)

        self.logger.info("Connection established.")

    # Bot message processor
    def messageHandler(self, conn, message):

        (reply, sendMessage, shutdown) = self.processor.getResponse(message)

        if sendMessage:
            conn.send(xmpp.Message(message.getFrom(), reply))

        if shutdown:
            self.status = False

    def initiate(self):

        # Initiate the message handler
        self.conn.RegisterHandler('message', self.messageHandler)

        # Put bot online
        self.conn.sendInitPresence()

        self.logger.info("Initiated.")

        while self.status:
            try:
                self.conn.Process(1)
            except KeyboardInterrupt:
                self.status = False

        self.logger.info("Shutdown complete.")

if __name__ == '__main__':

    if len(sys.argv)<3:
        print "Usage: jarvis.py username@server.net password"
        logger.error("Not enough arguments specified.\nPlease specify appropriate arguments")
    else:

        username = sys.argv[1]
        password = sys.argv[2]

        jarvisBot  = Jarvis()

        # Initiate connection
        jarvisBot.connect(username, password)

        # Begin the service iterator to keep the bot going until the close message is received
        jarvisBot.initiate()
