#! /bin/env cmsRun

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing("analysis")
options.setDefault('maxEvents', 10)
options.register(
  'lhesrc',
  'externalLHEProducer',
	VarParsing.multiplicity.singleton,
	VarParsing.varType.string,
	'global tag to be used'
)

options.parseArguments()

import FWCore.ParameterSet.Config as cms
process = cms.Process("NOTIMPORTANT")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
		options.inputFiles
		)
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.lheheader = cms.EDAnalyzer(
	'LHEHeaderDumper',
	src = cms.InputTag(options.lhesrc)
)
process.p = cms.Path(process.lheheader)
