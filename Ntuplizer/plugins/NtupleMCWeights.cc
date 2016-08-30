// -*- C++ -*-
//
// Package:    URNtuples/NtupleMCWeights.cc
// Class:      NtupleMCWeights.cc
// 
/**\class NtupleMCWeights.cc NtupleMCWeights.cc.cc URNtuples/NtupleMCWeights.cc/plugins/NtupleMCWeights.cc.cc

 Description: Add inheritance information to GenParticles and store it in the URTree.
              The inheritance information (mom_index) consists in assigning an integer counter to each 
	      GenParticle in the input collection that points to its mother.

 Useful to take a look at these pages, (I stole the bulk of the code from the second link):
 https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate
 https://cmssdt.cern.ch/SDT/lxr/source/PhysicsTools/HepMCCandAlgos/plugins/ParticleListDrawer.cc
*/
//
// Original Author:  Aran Garcia-Bellido
//         Created:  Wed, 22 Jan 2015 15:08:09 GMT
//
#include <vector>
#include <string>
#include <iostream>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "Math/VectorUtil.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Common/interface/Ref.h"
#include "URNtuples/Ntuplizer/interface/Obj2BranchBase.h"
#include "URNtuples/Ntuplizer/interface/ObjExpression.h" //defines the separator

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

class NtupleMCWeights : public Obj2BranchBase{
public:
  /// default constructor
  NtupleMCWeights(edm::ParameterSet iConfig);
  /// default destructor
  ~NtupleMCWeights();

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  // ----------member data ---------------------------
  bool isMC_;
  edm::InputTag src_;
  edm::EDGetTokenT<LHEEventProduct> srcToken_;
   
  std::vector<float> weights;
  int npnlo;
};

// Constructor
NtupleMCWeights::NtupleMCWeights(edm::ParameterSet iConfig): 
	Obj2BranchBase(iConfig),
	src_(iConfig.getParameter<edm::InputTag>("src")),
	srcToken_(consumes<LHEEventProduct>(src_))
	//weights(1)
{
  // By having this class inherit from Obj2BranchBAse, we have access to our tree_, no need for TFileService
  // Book branches:
  tree_.branch(prefix_+SEPARATOR+"weights", &weights); 
  tree_.branch(std::string("NPNLOLHE")+SEPARATOR+"npnlo", &npnlo, (std::string("NPNLOLHE")+SEPARATOR+"npnlo/I").c_str()); 
}

// Destructor
NtupleMCWeights::~NtupleMCWeights()
{
}

void NtupleMCWeights::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	weights.clear();

	edm::Handle<LHEEventProduct> lheinfo;
	iEvent.getByToken(srcToken_, lheinfo);
	if(lheinfo.isValid())
	{
		for(size_t w = 0 ; w < lheinfo->weights().size() ; ++w)
		{
			//weights[0].push_back(lheinfo->weights()[w].wgt);
			weights.push_back(lheinfo->weights()[w].wgt);
			//std::cout << w << " " << lheinfo->weights()[w].id << " " << lheinfo->weights()[w].wgt << std::endl;
		}
		npnlo = lheinfo->npNLO();
		//std::cout << npnlo << std::endl;
	} 
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(NtupleMCWeights);
