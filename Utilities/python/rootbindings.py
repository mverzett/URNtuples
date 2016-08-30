import os
import ROOT
ROOT.gSystem.Load("%s/external/src/RooUnfold/libRooUnfold.so" % os.environ['URA'])
ROOT.gSystem.Load("%s/external/src/TUnfold/libunfold.so" % os.environ['URA'])
#monkey patch to use the proper class
import re
regex = re.compile('TUnfold(?P<version>V\d+)\.cxx$')
cxx = [i for i in os.listdir("%s/external/src/TUnfold" % os.environ['URA']) if regex.match(i)][0]
version = regex.match(cxx).group('version')

headers = [i for i in os.listdir("%s/external/src/TUnfold" % os.environ['URA']) if i.endswith('.h') and not i.endswith('Dict.h')]
headers = [i[:-2] for i in headers]
for header in headers:
   setattr(
      ROOT, header,
      getattr(ROOT, header+version)
      )
     
