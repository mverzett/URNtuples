#! /bin/env cmsRun

#make it executable
from URAnalysis.Configuration.varparsing import options
import FWCore.ParameterSet.Config as cms
import URAnalysis.PATTools.custompat as urpat
import URAnalysis.PATTools.customskims as urskims
import URAnalysis.PATTools.meta  as meta
import URAnalysis.Ntuplizer.ntuplizer as ntuple

options.parseArguments()

process = cms.Process("PATPlusNtuple")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.cerr.FwkSummary.reportEvery = options.reportEvery

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options.globalTag

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(True)
)
process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(
      options.maxEvents
      )
)

process.source = cms.Source(
    "PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
      #'/store/relval/CMSSW_7_0_6/RelValTTbarLepton_13/MINIAODSIM/PLS170_V6AN1-v1/00000/CA50900E-43FA-E311-B663-0025905A48EC.root'
      options.inputFiles
      ),
)
if options.pick:
	process.source.eventsToProcess = cms.untracked.VEventRange(options.pick)

process.TFileService = cms.Service(
        "TFileService",
        fileName = cms.string(options.outputFile)
)

######################
##   PREPROCESSING
######################
collections = { 
   'muons' : 'slimmedMuons',
   'electrons' : 'slimmedElectrons',
   'photons' : 'slimmedPhotons',
   'jets' : 'slimmedJets',
   'vertices' : 'offlineSlimmedPrimaryVertices',
   'METs' : 'slimmedMETs',
   'NoHFMETs' : 'slimmedMETsNoHF',
   'genParticles' : 'prunedGenParticles',
   }
sequence, collections = urpat.preprocess(process, options, **collections)
process.preprocessing = sequence

#HF Noise Filter
process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999) 
process.preprocessing *= process.HBHENoiseFilterResultProducer

if not options.noSkim:
	skims = urskims.add_skims(process, **collections)
	if options.skims:
		if options.skims.lower() == 'help':
			for i in skims:
				print i.label_()
			raise RuntimeError('Everything is OK, just wanted to exit')
		else:
			to_pick = set(options.skims.split(','))
			skim_sequences = [i.label_() for i in skims]
			skim_sequences = filter(lambda x: x in to_pick, skim_sequences)
	else:
		skim_sequences = [i.label_() for i in skims]
else:
	skim_sequences = []

#store meta
process.load("Configuration.StandardSequences.Services_cff")
process.load('URAnalysis.Ntuplizer.MetaNtuplize_cfi')
process.metaTree.isMC = cms.bool(options.isMC)
process.meta = cms.Sequence(
   meta.embed_meta(process, options.isMC, options.computeWeighted and options.isMC) *
   process.metaTree
   )
process.metaTree.globalTag=process.GlobalTag.globaltag

#from pdb import set_trace
#set_trace()
#make custom PAT

custom_pat_sequence, collections = urpat.customize(
   process,
   options,
   **collections
)

ntuple_sequence, ntuple_end = ntuple.make_ntuple(
   process,
   options, 
   **collections
   )

process.schedule = cms.Schedule()
#make meta+skim+customPAT+Ntuple paths
#one for each skim sequence
#shared modules do not get rerun
#https://hypernews.cern.ch/HyperNews/CMS/get/edmFramework/3416/1.html

if skim_sequences:
   for skim in skim_sequences:
      path_name = skim+'Path0'
      #assure to make NEW path name
      idx = 1
      while hasattr(process, path_name):
         path_name = path_name[:-1]+str(idx)
         idx += 1
      setattr(
         process,
         path_name,
         cms.Path(
            process.meta *
            process.preprocessing *
            getattr(process, skim) *
            custom_pat_sequence *
            ntuple_sequence *
            ntuple_end
            )
         )
      process.schedule.append(
         getattr(process, path_name)
         )
else:
   process.passThroughPath = cms.Path(
      process.meta *
      process.preprocessing *
      custom_pat_sequence *
      ntuple_sequence *
      ntuple_end
      )
   process.schedule.append(process.passThroughPath)

if options.edm:
	process.edmOut = cms.OutputModule(
		"PoolOutputModule",
		# use this in case of filter available
		outputCommands = cms.untracked.vstring( 
			'drop *',
			'keep *_slimmedJets*_*_*',
			'keep *_jetsNewJECAllEmbedded_*_*',
			'keep *_METsNewJECAllEmbedded_*_*',
			'keep *_slimmedMETs*_*_*',
			),
		fileName = cms.untracked.string('edmTEST.root')
		)
	process.end = cms.EndPath(
		process.edmOut
		)
	process.schedule.append(process.end)
