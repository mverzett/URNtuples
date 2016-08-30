import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.source = cms.Source(
    "PoolSource",
    # replace 'myfile.root' with the source file you want to use                                                                                                                                                                          
    fileNames = cms.untracked.vstring(
        'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU30bx50_PHYS14_25_V1-v1/00000/003B6371-8D81-E411-8467-003048F0E826.root'
        #'/store/relval/CMSSW_7_0_6/RelValTTbarLepton_13/MINIAODSIM/PLS170_V6AN1-v1/00000/CA50900E-43FA-E311-B663-0025905A48EC.root'
        ),
    #skipEvents=cms.untracked.uint32(0)
)

#process.Tracer = cms.Service("Tracer")
process.TFileService = cms.Service(
        "TFileService",
        fileName = cms.string("test_ntuple.root")
)

# To print out the MC generator info for the first event:
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(1),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("prunedGenParticles")
)

import URAnalysis.Ntuplizer.ntuplizer as ntuplizer
ntuple_seq, ntuple_end = ntuplizer.make_ntuple(
   process,
   True
   )
   
# If you want to add you own analyzer, just add it like: ntuple_seq+process.printTree
process.p = cms.Path(ntuple_seq)
process.end = cms.EndPath(
   ntuple_end
)
process.schedule = cms.Schedule(
   process.p,
   process.end
)
