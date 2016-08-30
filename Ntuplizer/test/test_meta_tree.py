import FWCore.ParameterSet.Config as cms

process = cms.Process("testMetaTree")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use                                                                                                                                                                           
    fileNames = cms.untracked.vstring(
        'file:/afs/cern.ch/user/m/mverzett/work/framework/CMSSW_7_0_7_patch1/src/URAnalysis/PATTools/test/pat_test.root'
    )
)

process.load('Configuration.StandardSequences.Services_cff')
process.load('DQMServices.Components.EDMtoMEConverter_cfi')
process.load('URAnalysis.Ntuplizer.MetaNtuplize_cfi')

process.TFileService = cms.Service(
    "TFileService", 
    fileName = cms.string("test_meta_tree2.root") 
)

process.meta = cms.Sequence(
    process.EDMtoMEConverter +
    process.metaTree
)

process.p = cms.Path(process.meta)
process.schedule = cms.Schedule(process.p)
