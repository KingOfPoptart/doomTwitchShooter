import yaml
import socket
import re
import logging
import threading
from time import sleep
from os.path import expanduser
from sys import stdout


from twitch import twitch
from doomApiClient import doomApiClient
from twitchControlMap import twitchControlMap

def checkForRestart(doomClient):
  while True:
    print doomClient.getHealth()
    if doomClient.getHealth() < 0:
      #doomClient.restartMap(2,1)
      doomClient.startRandomLevel(3, 9)
    sleep(3)


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

d = doomApiClient()
cntrl = twitchControlMap(doomApiClient = d)


thread = threading.Thread(target=checkForRestart, args=((d,)))
thread.daemon = True
thread.start()

while run:
  response = t.getMsg()
  if response == t.getPing():
    t.pong()
  else:
    chatMessage = t.parseTwitchMessage(response)
    cntrl.parseAndAct(chatMessage['message'])
    
    #We are connected!
    if 'End of /NAMES list' in chatMessage['message']:
      connected = True
      logger.info('Connected!')
 
 
    if connected == True:  
      if 'End of /NAMES list' in chatMessage['message']:
          pass
      else:
        t.privmsg("Thanks "+chatMessage['username']+'!')

  #so we don't send messages too fast
  sleep(twitchConfig['sleepTime'])
