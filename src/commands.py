# !/usr/bin/python

# commands.py
# Pre-built command responses for Chatbot

def getResponse(message):

    # Parse the message
    text = message.getBody()
    user = message.getFrom()
    
    response = ''
    sendMessage = True
    shutdown = False
    
    # Parsing and decision-making
    if not text or text == '':
        sendMessage = False
    elif 'stop' in text.lower():
        shutdown = True
    else:
        response = "Ha HA! You said: '%s'" % text
        
    return (response, sendMessage, shutdown)