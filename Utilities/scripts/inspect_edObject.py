#! /usr/bin/env python

'''
Loads an ED event file (PAT, miniAOD, AOD, etc) and loads a collection you want to inspect,
leaves the interpreter open

Author: Mauro Verzetti UR
'''

from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument('file', help='file path')
parser.add_argument('handle', help='type of handle to be used')
parser.add_argument('label', help='label of collection to be inspected')
parser.add_argument('--pick', help='which single event to pick')
args = parser.parse_args()

pick = False
if args.pick:
	pick = tuple([int(i) for i in args.pick.split(':')])

import ROOT
import pprint
from DataFormats.FWLite import Events, Handle
from pdb import set_trace
ROOT.gROOT.SetBatch()

fname = args.file
if fname.startswith('/store/'):
   fname = 'root://cmsxrootd-site.fnal.gov/%s' % fname

events = Events(fname)
iterator = events.__iter__()
handle = Handle(args.handle)
keep_going = True
loop = 0

while keep_going:
	evt = iterator.next()
	loop += 1
	get_result = evt.getByLabel(args.label, handle)
	obj = handle.product()
	if pick:
		evtid = (evt.eventAuxiliary().run(), evt.eventAuxiliary().luminosityBlock(), evt.eventAuxiliary().event())
		if evtid == pick:
			keep_going = False
	else:
		print 'loop %d' % loop
		keep_going = not get_result
		if 'vector' in args.handle:
			keep_going = obj.size() == 0
	

print "object/collection successfully loaded into obj, entering debugging mode"
set_trace()
