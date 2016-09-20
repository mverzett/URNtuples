#! /bin/env python

import URNtuples.Utilities.prettyjson as prettyjson
import sys
from argparse import ArgumentParser
from pdb import set_trace
import os
import subprocess
from fnmatch import fnmatch
from glob import glob

parser = ArgumentParser()
parser.add_argument('sample', help='Sample to run on, POSIX regex allowed')
parser.add_argument('json', help='json file containing the samples definition')
parser.add_argument('--options', help='command-line arguments'
                    ' to be passed to the configuration', default="")

args = parser.parse_args()

def parse_pyargs(string):
   'parses the pyargs and builds a dictionary'
   if not string: return {}
   args = string.split(' ')
   return dict(
      tuple(arg.split('=')) for arg in args
      )

def dump_pyargs(kwargs):
   'geta a dictionary and dumps a string'
   return ' '.join([
         '%s=%s' % i for i in kwargs.iteritems()
         ])

if not os.path.isfile(args.json):
   raise ValueError('file %s does not exist' % args.json)

all_samples = prettyjson.loads(open(args.json).read())
to_submit = filter(
   lambda x: fnmatch(x['name'], args.sample),
	 all_samples
)
pyargs = parse_pyargs(args.options)

sample = None
if not len(to_submit):
	raise RuntimeError('Could not find any sample matching the pattern')
elif len(to_submit) > 1:
	print "Multiple matches were found!"
	for i, j in enumerate(to_submit):
		print i, '-->', j['name']
	idx = raw_input(' Which one should I pick? ')
	sample = to_submit[int(idx)]
else:
	sample = to_submit[0]
print "Testing execution of %s" % sample['name']


opts = {}
isData = sample['name'].startswith('data')
opts['isMC'] = 'True' if not isData else 'False'
opts['computeWeighted'] = 'True' if not isData else 'False'

if 'options' in sample:
	opts.update(sample['options'])
opts.update(pyargs)

print 'execute:'
cmd = ['cmsRun', 'make_pat_and_ntuples.py']
cmd.extend(['%s=%s' % i for i in opts.iteritems()])
cmd.append('inputFiles=')
print ' '.join(cmd)
