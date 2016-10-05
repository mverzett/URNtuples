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
	bool active_;
   
  std::vector<float> weights;
  int npnlo_;
	int procId_;
	double originalXWGTUP_;
};

// Constructor
NtupleMCWeights::NtupleMCWeights(edm::ParameterSet iConfig): 
	Obj2BranchBase(iConfig),
	src_(iConfig.getParameter<edm::InputTag>("src")),
	srcToken_(consumes<LHEEventProduct>(src_)),
	active_(iConfig.getParameter<bool>("active"))
	//weights(1)
{
	std::cout << "NtupleMCWeights::NtupleMCWeights" << std::endl;
  // By having this class inherit from Obj2BranchBAse, we have access to our tree_, no need for TFileService
  // Book branches:
  tree_.branch(prefix_+SEPARATOR+"weights", &weights); 
  tree_.branch(std::string("LHEInfo")+SEPARATOR+"npnlo", &npnlo_,  (std::string("LHEInfo")+SEPARATOR+"npnlo/I").c_str()); 
	tree_.branch(std::string("LHEInfo")+SEPARATOR+"procID", &procId_, (std::string("LHEInfo")+SEPARATOR+"procID/I").c_str());
	tree_.branch(std::string("LHEInfo")+SEPARATOR+"LHEWeight", &originalXWGTUP_, (std::string("LHEInfo")+SEPARATOR+"LHEWeight/D").c_str());
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
	if(!active_) return;

	for(size_t w = 0 ; w < lheinfo->weights().size() ; ++w)
	{
		//weights[0].push_back(lheinfo->weights()[w].wgt);
		weights.push_back(lheinfo->weights()[w].wgt);
		//std::cout << w << " " << lheinfo->weights()[w].id << " " << lheinfo->weights()[w].wgt << std::endl;
	}
	npnlo_ = lheinfo->npNLO();
	procId_ = lheinfo->hepeup().IDPRUP;
	originalXWGTUP_ = lheinfo->originalXWGTUP();
	//std::cout << lheinfo->hepeup().IDPRUP << std::endl;
	//std::cout << npnlo << std::endl;
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(NtupleMCWeights);
