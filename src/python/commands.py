# !/usr/bin/python

# commands.py
# Pre-built command responses for Jarvis Chatbot

import urllib2

class MessageProcessor:

    # Wolfram Alpha APP ID
    #__APP_ID__ = "798T52-TWLAW7UVXJ"
    # Query format: http://api.wolframalpha.com/v2/query?input=pi&appid=XXXX

    def __init__(self, logger):
        self.activeUsers = {}
        self.logger = logger

        self.__opener__ = urllib2.build_opener()
        self.__opener__.addheaders = [('User-agent', 'Mozilla/5.0')]

    def getResponse(self, message):

        # Parse the message
        text = message.getBody()
        user_full_str = message.getFrom()
        user = str(user_full_str).split("/")[0]

        # Commands
        shutdown_phrases = ['shutdown','shut down']

        # Setup
        response = ''
        sendMessage = True
        shutdown = False

        # Parsing and decision-making
        if user not in self.activeUsers:
            response = 'Good day sir. What can I do for you?'
            self.activeUsers[user] = [text]
            self.logger.info('New user added: %s (%s)' % (user, text))

        # Blank message
        elif not text or text == '':
            sendMessage = False

        # Shutdown
        elif any([phrase in text.lower() for phrase in shutdown_phrases]):
            response = 'Thank you, enjoy your day sir.'
            self.activeUsers.pop(user)
            self.logger.info('Shutdown command received from %s (%s)' % (user, text))
            shutdown = True

        # Default
        else:

            request = text.replace(' ', '%20')

            infile = self.__opener__.open('http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=%s' % request)
            page = infile.read()

            response = page
            self.activeUsers[user].append(text)
            self.logger.info('%s: %s' % (user, text))

        return (response, sendMessage, shutdown)