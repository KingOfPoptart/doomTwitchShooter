from os.path import expanduser
from sys import stdout
import yaml
import socket
import re
import time
import logging



class twitch:
  def __init__( self, host, port, channel, 
                ircPing='tmi.twitch.tv', 
                chatMsgRgx=r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :" ):
    self.logger = logging.getLogger('twitchChatClient')
    self.s = socket.socket()
    self.host = host
    self. port = port
    self.channel = channel
    self.ircPing = ircPing
    self.chatMsgRgx = chatMsgRgx
    

  def connect(self):
    self.s.connect((self.host, self.port))
    
  def _send(self, msg):
    toSend = (msg+"\r\n").encode("utf-8")
    self.logger.info("Message to send: "+toSend.strip())
    byteSize = self.s.send(toSend)
    self.logger.info("Sent "+str(byteSize)+" bytes")

  def getPing(self):
    pingMsg = "PING :"+self.ircPing+"\r\n"
    self.logger.info(pingMsg.strip())
    return pingMsg

  def pong(self):
    self._send("PONG :"+self.ircPing)

  def passOauth(self, oauth):
    self._send("PASS {}\r\n".format('oauth:'+oauth))

  def join(self):
    self._send("JOIN #{}\r\n".format(self.channel))

  def nick(self, username):
    self._send("NICK {}\r\n".format(username))

  def privmsg(self, msg):
    self._send('PRIVMSG #{}\r\n'.format(self.channel+" :"+msg))


  def getMsg(self, size=2048):
    response = self.s.recv(2048).decode("utf-8")
    self.logger.info("Got response: "+response.strip())
    return response

  def parseTwitchMessage(self, response):
    username = re.search(r"\w+", response).group(0)
    CHAT_MSG = re.compile(self.chatMsgRgx)
    message = CHAT_MSG.sub("", response).rstrip('\n')
    self.logger.info(username.title() + ':'+ message.strip())
    return { 
              "username": username.title(), 
              "message": message
            }

  def connectAndJoin(self, oauth, username):
    self.connect()
    self.passOauth(oauth)
    self.nick(username)
    self.join()

















