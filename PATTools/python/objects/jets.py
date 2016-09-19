import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatUtils.patPFMETCorrections_cff import patSmearedJets

def add_jets(process, collection, opts):
	process.urSkimmedJets = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag(collection),
    cut = cms.string('pt > 20 && abs(eta) < 4')
		)

	process.customJets = cms.Sequence(
		process.urSkimmedJets
		)
	return process.customJets, 'urSkimmedJets'
	
