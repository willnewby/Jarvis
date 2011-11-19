#!/usr/bin/python
# -*- coding: koi8-r -*-
# $Id: bot.py,v 1.2 2006/10/06 12:30:42 normanr Exp $
# Based on framework at http://xmpppy.sourceforge.net/examples/bot.py
import sys
import xmpp
import commands
import logging

# Global status, indicating whether to continue
# It's not threadsafe, but whatever
status = True

# Bot message processor
def messageHandler(conn, message):
    
    (reply, sendMessage, shutdown) = commands.getResponse(message)
    
    if shutdown:
        print "Stop message received: shutting down bot."
        global status
        status = False
    elif sendMessage:
        conn.send(xmpp.Message(message.getFrom(), reply))
    
def serviceIterator(conn):

    global status
    while status:
        try:
            conn.Process(1)
        except KeyboardInterrupt:
            status = False

if __name__ == '__main__':

    logger = logging.getLogger('Jarvis')

    if len(sys.argv)<3:
        print "Usage: jarvis.py username@server.net password"
        logger.error("Not enough arguments specified.")
    else
        jarvis()
        
    jid = xmpp.protocol.JID(sys.argv[1])
    user = jid.getNode()
    server = jid.getDomain()
    password = sys.argv[2]

    conn = xmpp.Client(server,debug=[])
    conres = conn.connect(("talk.google.com", 5222))
    
    if not conres:
        print "Unable to connect to server %s!" % server
        sys.exit(1)
    if conres<>'tls':
        print "Warning: unable to estabilish secure connection - TLS failed!"
    authres=conn.auth(user,password)
    if not authres:
        print "Unable to authorize on %s - check login/password." % server
        sys.exit(1)
    if authres<>'sasl':
        print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
    
    # Initiate the message handler
    conn.RegisterHandler('message',messageHandler)
    
    # Put bot online
    conn.sendInitPresence()
    
    print "Good day sir."
    
    # Begin the service iterator to keep the bot going until the close message is received
    serviceIterator(conn)
    
    print "Shutting down bot."