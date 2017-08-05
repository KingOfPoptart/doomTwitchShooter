from os.path import expanduser
from sys import stdout
import yaml
import socket
import re
import time
import logging

from twitch import twitch




#Defaults
defaultTwitchConfigFile = expanduser('~/.twitch')


#Load configs
twitchConfig = yaml.load(open(defaultTwitchConfigFile, "r"))


t = twitch( host = twitchConfig["twitch"]["host"], 
            port = twitchConfig["twitch"]["port"], 
            channel = twitchConfig['chat']['channel'],
            ircPing = twitchConfig["twitch"]["ircPing"], 
            chatMsgRgx = twitchConfig["chat"]["chatMessageRegex"])



logging.basicConfig(stream=stdout, level=logging.INFO)
logger = logging.getLogger('doomTwitchShooter')

t.connectAndJoin( oauth = twitchConfig["chat"]["oauth"], 
                  username = twitchConfig["chat"]["username"])

connected = False
run = True


while run:
  response = t.getMsg()
  if response == t.getPing():
    t.pong()
  else:
    chatMessage = t.parseTwitchMessage(response)
    #We are connected!
    if 'End of /NAMES list' in chatMessage['message']:
      connected = True
      logger.info('Connected!')
 
 
    if connected == True:  
      if 'End of /NAMES list' in chatMessage['message']:
          pass
      else:
        t.privmsg("Right back at ya!")
 

  #so we don't send messages too fast
  time.sleep(twitchConfig['sleepTime'])
