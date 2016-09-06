import FWCore.ParameterSet.Config as cms
from URNtuples.PATTools.objects.trigger import mu_trg, el_trg
from pdb import set_trace

def add_skims(process, **collections):
	'''returns a list of added sequences'''
	process.muTrg = cms.EDFilter(
		'TriggerResultsFilter',
		hltResults = cms.InputTag(collections['triggerResults']),
		throw = cms.bool(False), #if the trigger is not there do not get mad!
		l1tResults = cms.InputTag(""),
		l1tIgnoreMask = cms.bool(True),
		l1techIgnorePrescales = cms.bool(True),
		triggerConditions = cms.vstring(*['%s_v*' % i for i in mu_trg])
		)

	process.hiptMuons = cms.EDFilter(
		"PATMuonSelector",
		src = cms.InputTag(collections['muons']),
		cut = cms.string('pt > 20 && abs(eta) < 2.5')
		)
	
	process.oneMuonFilter = cms.EDFilter(
	 "CandViewCountFilter",
	 src = cms.InputTag('hiptMuons'),
	 minNumber = cms.uint32(1)
	 )
	
	process.elTrg = process.muTrg.clone(
		triggerConditions = cms.vstring(*['%s_v*' % i for i in el_trg])
		)

	process.hiptElectrons = cms.EDFilter(
		"PATElectronSelector",
		src = cms.InputTag(collections['electrons']),
		cut = cms.string('pt > 20 && abs(eta) < 2.5')
		)
	
	process.oneElectronFilter = cms.EDFilter(
		"CandViewCountFilter",
		src = cms.InputTag('hiptElectrons'),
		minNumber = cms.uint32(1)
		)
	
	process.hiPtJets = cms.EDFilter(
		"PATJetSelector",
		src = cms.InputTag(collections['jets']),
		cut = cms.string('pt > 20 && abs(eta) < 10')
	)
	
	process.threeJetFilter = cms.EDFilter(
		"CandViewCountFilter",
		src = cms.InputTag('hiPtJets'),
		minNumber = cms.uint32(3)
		)
	
	process.fourJetFilter = cms.EDFilter(
		"CandViewCountFilter",
		src = cms.InputTag('hiPtJets'),
		minNumber = cms.uint32(3)
		)
	
	process.muPlus4Jets = cms.Sequence(
		process.hiptMuons *
		process.oneMuonFilter *
		process.hiPtJets *
		process.fourJetFilter
		)
	
	process.trgMuPlus4Jets = cms.Sequence(
		process.muTrg *
		process.muPlus4Jets
		)

	process.muPlus3Jets = cms.Sequence(
		process.hiptMuons *
		process.oneMuonFilter *
		process.hiPtJets *
		process.threeJetFilter
		)
	
	process.trgMuPlus3Jets = cms.Sequence(
		process.muTrg *
		process.muPlus3Jets
		)

	process.elPlus4Jets = cms.Sequence(
		process.hiptElectrons *
		process.oneElectronFilter *
		process.hiPtJets *
		process.fourJetFilter
		)
	
	process.trgElPlus4Jets = cms.Sequence(
		process.elTrg *
		process.elPlus4Jets
		)

	process.elPlus3Jets = cms.Sequence(
		process.hiptElectrons *
		process.oneElectronFilter *
		process.hiPtJets *
		process.threeJetFilter
		)

	process.trgElPlus3Jets = cms.Sequence(
    process.elTrg *
    process.elPlus3Jets
    )

	
	return [
		process.muPlus4Jets,
		process.trgMuPlus4Jets,
		process.muPlus3Jets,
		process.trgMuPlus3Jets,
		process.elPlus4Jets,
		process.trgElPlus4Jets,
		process.elPlus3Jets,
		process.trgElPlus3Jets
		]

