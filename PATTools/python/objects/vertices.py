import FWCore.ParameterSet.Config as cms

urVertices = cms.EDFilter(
   "VertexSelector",
   src=cms.InputTag('fixme'),
   cut=cms.string("isValid & ndof >= 4 && abs(z) < 24 && position.Rho < 2.0"),
   filter=cms.bool(True), #allow to terminate path if no usable vtx is found
)
customVertices = cms.Sequence(
   urVertices
)
