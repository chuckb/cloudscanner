import sys
import threading
import time

class ResettableTimer(threading.Thread):
  """
  The ResettableTimer class is a timer whose counting loop can be reset
  arbitrarily. Its duration is configurable. Commands can be specified
  for both expiration and update. Its update resolution can also be
  specified. Resettable timer keeps counting until the "run" method
  is explicitly killed with the "kill" method.
  """
  def __init__(self, maxtime, expire, inc=None, update=None):
    """
    @param maxtime: time in seconds before expiration after resetting
                    in seconds
    @param expire: function called when timer expires
    @param inc: amount by which timer increments before
                updating in seconds, default is maxtime/2
    @param update: function called when timer updates
    """
    self.maxtime = maxtime
    self.expire = expire
    if inc:
      self.inc = inc
    else:
      self.inc = maxtime/2
    if update:
      self.update = update
    else:
      self.update = lambda c : None
    self.counter = 0
    self.active = True
    self.stop = False
    threading.Thread.__init__(self)
    self.setDaemon(True)
  def set_counter(self, t):
    """
    Set self.counter to t.

    @param t: new counter value
    """
    self.counter = t
  def deactivate(self):
    """
    Set self.active to False.
    """
    self.active = False
  def kill(self):
    """
    Will stop the counting loop before next update.
    """
    self.stop = True
  def reset(self):
    """
    Fully rewinds the timer and makes the timer active, such that
    the expire and update commands will be called when appropriate.
    """
    self.counter = 0
    self.active = True

  def run(self):
    """
    Run the timer loop.
    """
    while True:
      self.counter = 0
      while self.counter < self.maxtime:
        self.counter += self.inc
        time.sleep(self.inc)
        if self.stop:
          return
        if self.active:
          self.update(self.counter)
      if self.active:
        self.expire()
        self.active = False

