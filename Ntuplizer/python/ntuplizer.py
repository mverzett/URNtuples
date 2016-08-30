import FWCore.ParameterSet.Config as cms
import URAnalysis.Ntuplizer.branches as branches
from URAnalysis.PATTools.objects.trigger import trigger_paths

def make_ntuple(process, opts, ntuple_seq_name='ntuple', **kwargs):
	'''
	Function to customize the process and add the Ntuple
	production sequence as ntuple_seq_name (default 'ntuple').
	keyword args can be passed to modify the source of each
	Ntuple object, the keyword is the ntuple object name
	returns a tuple: (ntuple_sequence, ntuple_end_module)
	'''
	process.ntupleEnd = cms.EDAnalyzer('TreeFiller')
	if not hasattr(process, ntuple_seq_name):
		setattr(process, ntuple_seq_name, cms.Sequence())
		ntuple = getattr(process, ntuple_seq_name)
	if not isinstance(ntuple, cms.Sequence):
		raise ValueError(
			'The process already has module named '
			'"ntuple", which is not a cms.Sequence, '
			'please choose a different name while builing'
			'the ntuple'
			)
	
	process.evtid = cms.EDAnalyzer(
		'EvtIDProducer'
		)
	ntuple += process.evtid
	
	process.trigger = cms.EDAnalyzer(
		'NtupleTrigger',
		trigger = cms.InputTag('TriggerResults', '', 'HLT'),
		prescales = cms.InputTag('patTrigger'),
		triggerSelection = cms.vstring(trigger_paths),
		branches = cms.VPSet(
			)
		)
	if opts.reHLT:
		process.trigger.trigger = cms.InputTag('TriggerResults', '', 'HLT2')
	ntuple += process.trigger
	
	process.filter = cms.EDAnalyzer(
		'NtupleFilter',
		filterSelection = cms.vstring("Flag_goodVertices", "Flag_CSCTightHaloFilter", "Flag_trkPOGFilters", "Flag_trkPOG_logErrorTooManyClusters", "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_ecalLaserCorrFilter", "Flag_trkPOG_manystripclus53X", "Flag_eeBadScFilter", "Flag_METFilters", "Flag_HBHENoiseFilter", "Flag_trkPOG_toomanystripclus53X", "Flag_hcalLaserEventFilter"),
		branches = cms.VPSet(
			)
		)
	ntuple += process.filter
	
	process.rho = cms.EDAnalyzer(
		'NtupleDoubleProducer',
		src = cms.InputTag(
			kwargs.get(
				'rho',
				'fixedGridRhoFastjetAll'
				)
			),
		branches = cms.VPSet(
			branches.make_branch_pset('value'))
		)
	ntuple += process.rho
	
	process.muons = cms.EDAnalyzer(
		'NtupleMuonsProducer',
		src = cms.InputTag(
			kwargs.get(
				'muons',
				'slimmedMuons'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.vertex_info +
			branches.isolation +
			branches.muon_specific
			)
		)
	ntuple += process.muons
	
	process.jets = cms.EDAnalyzer(
		'NtupleJetsProducer',
		src = cms.InputTag(
			kwargs.get(
				'jets',
				'slimmedJets'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.jet_specific +
			branches.btaggging +
			branches.jet_specific_mc
			)
		)
	ntuple += process.jets

	if opts.makeJetTracks:
		process.jets_tracks = cms.EDAnalyzer(
			'NtupleJetTracksProducer',
			src = cms.InputTag(
				kwargs.get(
					'jets',
					'slimmedJets'
					)
				),
			label = cms.string('jets'),
			)
		ntuple += process.jets_tracks
		
	process.electrons = cms.EDAnalyzer(
		'NtupleElectronsProducer',
		src = cms.InputTag(
			kwargs.get(
				'electrons',
				'slimmedElectrons'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.isolation +
			branches.vertex_info +
			branches.electron_specific +
			branches.ecal_cluster_specific +
			branches.super_cluster_specific
			)
		)
	ntuple += process.electrons
	
	process.photons = cms.EDAnalyzer(
		'NtuplePhotonsProducer',
		src = cms.InputTag(
			kwargs.get(
				'photons',
				'slimmedPhotons'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.super_cluster_specific +
			branches.photon_specific
			)
		)
	ntuple += process.photons
	
	process.vertexs = cms.EDAnalyzer(
		'NtupleVerticesProducer',
		src = cms.InputTag(
			kwargs.get(
				'vertexs',
				'offlineSlimmedPrimaryVertices'
				)
			),
		branches = cms.VPSet(
			branches.vertex_specific
			)
		)
	ntuple += process.vertexs
	
	if opts.useHFMET:
		process.NoHFMETs = cms.EDAnalyzer(
			'NtupleMETUncertainty',
			src = cms.InputTag(
				kwargs.get(
					'NoHFMETs',
					'slimmedMETsNoHF'
					)
				),
			)
		ntuple += process.NoHFMETs
	else:
		process.METs = cms.EDAnalyzer(
			'NtupleMETUncertainty',
			src = cms.InputTag(
				kwargs.get(
					'METs',
					'slimmedMETs'
					)
				),
			useUserCands = cms.bool(opts.runJEC),
			isMC = cms.bool(opts.isMC)
			)
		ntuple += process.METs
		
	#############
	#  MC Only info, on data will produce empty collections
	#############
	##if not opts.isMC:
	##	return ntuple, process.ntupleEnd
	process.genInfo = cms.EDAnalyzer(
		'NtupleGenInfoProducer',
		src = cms.InputTag(
			kwargs.get(
				'genInfo',
				'generator'
				)
			),
		branches = cms.VPSet(
			branches.geninfo_scpecific
			)
		)
	ntuple += process.genInfo
	
	process.MCWeights = cms.EDAnalyzer(
		'NtupleMCWeights',
		src = cms.InputTag(
			kwargs.get(
				'MCWeigths',
				'externalLHEProducer'
				)
			),
		branches = cms.VPSet(
			),
		computeWeighted = cms.bool(opts.computeWeighted)
		)
	ntuple += process.MCWeights
	
	process.PUInfos = cms.EDAnalyzer(
		'NtuplePUInfoProducer',
		src = cms.InputTag(
			kwargs.get(
				'PUInfos',
				'slimmedAddPileupInfo'
				)
			),
		branches = cms.VPSet(
			branches.puinfo_specific
			)
		)
	ntuple += process.PUInfos
	
	#genMET = cms.EDAnalyzer(
	process.genParticles = cms.EDAnalyzer(
		'NtupleGenParticlesProducer',
		src = cms.InputTag(
			kwargs.get(
				'genParticles',
				'prunedGenParticles'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.gen_particle_specific
			)
		)
	ntuple += process.genParticles
	
	if opts.storeLHEParticles:
		process.LHEPaticles = cms.EDAnalyzer(
			'NtupleLHEParticles',
			src = cms.InputTag(
				kwargs.get(
					'MCWeigths',
					'externalLHEProducer'
					)
				)
			)
		ntuple += process.LHEPaticles

	###### pseudo top test!!
	if opts.makePSTop:
		process.PSTjets = cms.EDAnalyzer(
			'NtupleGenJetsProducer',
			src = cms.InputTag(
				kwargs.get(
					'PSTjets',
					'pseudoTop:jets'
					)
				),
			branches = cms.VPSet(
				branches.kinematics +
				branches.genjet_specific
				)
			)
		ntuple += process.PSTjets
		
		process.PSTleptons = cms.EDAnalyzer(
			'NtupleGenJetsProducer',
			src = cms.InputTag(
				kwargs.get(
					'PSTleptons',
					'pseudoTop:leptons'
					)
				),
			branches = cms.VPSet(
				branches.kinematics +
				branches.genjet_specific
				)
			)
		ntuple += process.PSTleptons	
		
		process.PSTs = cms.EDAnalyzer(
			'NtupleGenParticlesProducer',
			src = cms.InputTag(
				kwargs.get(
					'PSTs',
					'pseudoTop'
					)
				),
			branches = cms.VPSet(
				branches.kinematics +
				branches.gen_particle_specific
				)
			)
		ntuple += process.PSTs
		
		process.PSTneutrinos = cms.EDAnalyzer(
			'NtupleGenParticlesProducer',
			src = cms.InputTag(
				kwargs.get(
                                  'PSTneutrinos',
                                  'pseudoTop:neutrinos'
                                  )
				),
			branches = cms.VPSet(
				branches.kinematics +
				branches.gen_particle_specific
				)
			)
		ntuple += process.PSTneutrinos
	
	process.genPInheritance = cms.EDAnalyzer(
		'NtupleGenParticleInheritance',
		label = cms.string('genParticles'),
		src = cms.InputTag('prunedGenParticles'),
		)
	ntuple += process.genPInheritance
	
	process.genjets = cms.EDAnalyzer(
		'NtupleGenJetsProducer',
		src = cms.InputTag(
			kwargs.get(
				'genjets',
				'slimmedGenJets'
				)
			),
		branches = cms.VPSet(
			branches.kinematics +
			branches.genjet_specific
			)
		)
	ntuple += process.genjets
	
	return ntuple, process.ntupleEnd
