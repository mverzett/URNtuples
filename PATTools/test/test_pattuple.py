import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source(
    "PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_7_0_6/RelValTTbarLepton_13/MINIAODSIM/PLS170_V6AN1-v1/00000/CA50900E-43FA-E311-B663-0025905A48EC.root'
        ),
    skipEvents=cms.untracked.uint32(15)
)

from URAnalysis.PATTools.customize_pat_production import customize

schedule = customize(process, True, meta2edm=True)

process.load('DQMServices.Components.MEtoEDMConverter_cfi')
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName=cms.untracked.string('pat_test_2.root'),
    #outputCommands=cms.untracked.vstring(output_command)
)
process.outpath = cms.EndPath(
    process.MEtoEDMConverter *
    process.out
)

process.schedule.append(process.outpath)

