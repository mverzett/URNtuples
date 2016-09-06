import FWCore.ParameterSet.Config as cms

###
# variables used by other modules, but here for consistency
###

mu_trg = [
	#single
	'HLT_IsoMu18',
	'HLT_IsoMu20',
	'HLT_IsoTkMu20',
	'HLT_IsoMu20_eta2p1',
	'HLT_IsoMu22',
	'HLT_IsoTkMu22',
	'HLT_IsoMu24',
	'HLT_IsoTkMu24',
	'HLT_IsoMu24_eta2p1',
	'HLT_IsoMu27',
	'HLT_IsoTkMu27',
	'HLT_Mu45_eta2p1',
	'HLT_Mu50',
	#double
	'HLT_DoubleIsoMu17_eta2p1',
	'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
	'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
]

el_trg = [
	#electrons
	#single
	'HLT_Ele22_eta2p1_WPLoose_Gsf',
	'HLT_Ele23_WPLoose_Gsf',
	'HLT_Ele27_WPLoose_Gsf',
	'HLT_Ele27_eta2p1_WPLoose_Gsf',
	'HLT_Ele27_WPTight_Gsf',
	'Ele27_eta2p1_WPLoose_Gsf_HT200', #with HT!
	'HLT_Ele32_eta2p1_WPTight_Gsf',
	'Ele35_WPLoose_Gsf',
	#double	
	'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL',
	'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
]

dummy_trg = [
	'HLT_notexists',
	]

trigger_paths = mu_trg + el_trg + dummy_trg

matchtemplate = cms.EDProducer(
   "PATTriggerMatcherDRDPtLessByR",
   src     = cms.InputTag('urSkimmedMuons'),
   #made in trigger.py
   matched = cms.InputTag('unpackedPatTrigger'),
   matchedCuts = cms.string('path("HLT_%s_v*") || type("TriggerMuon")'),
   maxDPtRel = cms.double(0.5),
   maxDeltaR = cms.double(0.5),
   resolveAmbiguities    = cms.bool(True),
   resolveByMatchQuality = cms.bool(True),
   #ensure we do not chain it as it makes an 
   #association map
   noSeqChain = cms.bool(True),
)

#unpacks trigger names, this module does not
#respect any coding convention, no src or similar,
#just leave it hardcoded and hope for the best!
from PhysicsTools.PatAlgos.slimming.unpackedPatTrigger_cfi import unpackedPatTrigger

customTrigger = cms.Sequence(
   unpackedPatTrigger
#   triggerEvent
)
