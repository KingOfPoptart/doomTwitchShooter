import requests
import logging
from sys import stdout
from random import randint

playerApi = 'player'
actionApi = 'player/actions'
worldApi = 'world'

class doomApiClient:

  

  def __init__( self, 
                host = "http://localhost", 
                port=6666, 
                apiPath = '/api/'):
    self.host = host+':'+str(port)
    self.apiPath = apiPath
    self.logger = logging.getLogger('doomApiClient')

  def buildUrl(self, path,):
    return self.host+self.apiPath+path



  def _get(self,path):
    builtUrl = self.buildUrl(path)
    self.logger.info('GET: '+builtUrl)
    r = requests.get(builtUrl)
    self.logger.info("Status code: " + str(r.status_code))
    self.logger.info("Response: "+ r.text)
    return r

  def _post(self, path, json=None):
    builtUrl = self.buildUrl(path)
    self.logger.info('POST: '+builtUrl)
    self.logger.info('POST json: '+str(json))
    r = requests.post(builtUrl, json=json)
    self.logger.info("Status code: " + str(r.status_code))
    self.logger.info("Response: "+ r.text)
    return r

  def _patch(self, path, json=None):
    builtUrl = self.buildUrl(path)
    self.logger.info('POST: '+builtUrl)
    self.logger.info('POST json: '+str(json))
    r = requests.patch(builtUrl, json=json)
    self.logger.info("Status code: " + str(r.status_code))
    self.logger.info("Response: "+ r.text)
    return r

  def shoot(self):
    self._post(actionApi, {"type": "shoot"})

  def mvForward(self):
    self._post(actionApi, {"type": "forward"})

  def mvBackward(self):
    self._post(actionApi, {"type": "backward"})

  def mvTurnLeft(self):
    self._post(actionApi, {"type": "turn-left"})

  def mvTurnRight(self):
    self._post(actionApi, {"type": "turn-right"})

  def open(self):
    self._post(actionApi, {"type": "open"})

  def weaponSwitch(self, weaponNum = 3):
    self._patch(playerApi, {"weapon": weaponNum})

  def getHealth(self):
    return self._get(playerApi).json()['health']

  def toggleGodMode(self):
    try:
      self._get(playerApi).json()['cheatFlags']['CF_GODMODE']
      self._patch(playerApi, {"cheatFlags":{"CF_GODMODE":False}})
    except:
      self._patch(playerApi, {"cheatFlags":{"CF_GODMODE":True}})

  def restartMap(self, map = 1, episode = 1):
    self._patch(worldApi , { 
                            "map" : map, 
                            "episode" : episode
                          })

  def startRandomLevel(self, EpisodeLimit = 3, mapLimit = 9):
    self._patch(worldApi , { 
                            "episode" : randint(1, EpisodeLimit),
                            "map" : randint(1, mapLimit)
                          })



if __name__ == "__main__":
  logging.basicConfig(stream=stdout, level=logging.INFO)
  d = doomApiClient()
  #d.open()
  d.startRandomLevel()

  #d.shoot()

  #d.mvTurnRight()
  #d.mvTurnLeft()
  #d.mvForward()
  #d.mvBackward()
