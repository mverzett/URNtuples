from fnmatch import fnmatch

def fnselect(samples, pattern, key=None):
   '''
   fnselect(samples, pattern, key=None) -> slected_samples
   selects a sample according to a POSIX pattern, if key
   is specified, the attribute key is used for selection
   '''
   if not key:
      return [i for i in samples if fnmatch(i, pattern)]
   else:
      return [i for i in samples if fnmatch(key(i), pattern)]
