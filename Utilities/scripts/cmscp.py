#! /bin/env cmsRun

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing("analysis")
options.setDefault('maxEvents', 100)
options.setDefault('outputFile', 'copy.root')
options.parseArguments()

import FWCore.ParameterSet.Config as cms
process = cms.Process("NOTIMPORTANT")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
		options.inputFiles
		)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.out = cms.OutputModule(
	"PoolOutputModule",
	outputCommands = cms.untracked.vstring('keep *'),
	fileName = cms.untracked.string(options.outputFile)
	)
process.end = cms.EndPath(process.out)
