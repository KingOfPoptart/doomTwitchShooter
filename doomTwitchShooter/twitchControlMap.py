import re

class twitchControlMap():
  
  def __init__(self, doomApiClient):
    self.doomApiClient = doomApiClient

  def parseAndAct(self, message):
    if re.match("f", message):
      self.doomApiClient.shoot()
    
    elif re.match("w", message):
      self.doomApiClient.mvForward()
    
    elif re.match("s", message):
      self.doomApiClient.mvBackward()
    
    elif re.match("a", message):
      self.doomApiClient.mvTurnLeft()
    elif re.match("d", message):
      self.doomApiClient.mvTurnRight()
    elif re.match("e", message):
      self.doomApiClient.open()
    elif re.match("[0-9]", message):
      self.doomApiClient.weaponSwitch(int(message.strip()))
    elif re.match("god", message):
      self.doomApiClient.toggleGodMode()
    elif re.match("restart", message):
      self.doomApiClient.startRandomLevel()


if __name__ == "__main__":
  from doomApiClient import doomApiClient
  d = doomApiClient()
  t = twitchControlMap(d)
  t.parseAndAct("shoot")
  