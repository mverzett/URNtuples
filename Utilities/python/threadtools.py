'''
Python threading helpers 
'''

import threading

class LockedObject(object):
   '''Simple implementation of an object                                                                                                                 
   shared beween threads.'''
   def __init__(self, item):
      self.object = item
      self.lock = threading.Lock()

   def __enter__(self):
      self.lock.acquire()
      return self.object

   def __exit__(self, type_, value, traceback):
      #check if any error occurred and raise it
      self.lock.release()
      return False
