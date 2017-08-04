from os.path import expanduser
from sys import stdout
import yaml
import socket
import re
import time
import logging


#Defaults
defaultTwitchConfigFile = expanduser('~/.twitch')
#configFile = expanduser('~/.doomTwitchShooter.yml')

#Load configs
twitchConfig = yaml.load(open(defaultTwitchConfigFile, "r"))
#config = yaml.load(open(configFile, "r"))

logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger('doomTwitchShooter')


sleepTime = 1

s = socket.socket()
s.connect((twitchConfig["twitch"]["host"], twitchConfig["twitch"]["port"]))

channel = twitchConfig["chat"]["channel"]

#oauth token
#Get from - https://twitchapps.com/tmi/
s.send("PASS {}\r\n".format('oauth:'+twitchConfig["chat"]["oauth"]).encode("utf-8"))
s.send("NICK {}\r\n".format(twitchConfig["chat"]["user"]).encode("utf-8"))
s.send("JOIN #{}\r\n".format(twitchConfig["chat"]["channel"]).encode("utf-8"))


connected = False
run = True
 
 
while run:
    response = s.recv(2048).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        put.red('Pong')
    else:
        logger.info(response)
        username = re.search(r"\w+", response).group(0)
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
       
        message = CHAT_MSG.sub("", response).rstrip('\n')
        
        #We are connected!
        if 'End of /NAMES list' in message:
            connected = True
            logger.info('Listening to '+channel)
 
 
        if connected == True:  
            if 'End of /NAMES list' in message:
                pass
            else:
                #Receive messages
                logger.info(username.title() + ':'+ message)

                #Send a message back
                byteSize = s.send('PRIVMSG #{}\r\n'.format(channel+" :Right back at ya!").encode("utf-8"))
                logger.info("Sent "+str(byteSize)+" bytes")
 
 
        #so we don't send messages too fast
        time.sleep(sleepTime)
