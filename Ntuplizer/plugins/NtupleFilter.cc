// -*- C++ -*-
//
// Package:    URNtuples/NtupleFilter.cc
// Class:      NtupleFilter.cc
// 
/**\class NtupleFilter.cc NtupleFilter.cc.cc URNtuples/NtupleFilter.cc/plugins/NtupleFilter.cc.cc

*/
//
// Original Author:  Aran Garcia-Bellido
//         Created:  Wed, 22 Jan 2015 15:08:09 GMT
//
#include <vector>
#include <string>
#include <iostream>
#include <regex>

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


#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

using namespace std;

class NtupleFilter : public Obj2BranchBase{
public:
	/// default constructor
	NtupleFilter(edm::ParameterSet iConfig);
	/// default destructor
	~NtupleFilter();

private:
	virtual void analyze(const edm::Event&, const edm::EventSetup&);

	// ----------member data ---------------------------
	bool isMC_;
	vector<string> triggerSelection_;
	edm::EDGetTokenT<edm::TriggerResults> src_;
	uint32_t currentrun_;
	vector<edm::EDGetTokenT<bool> > bool_tokens_;
	vector<int> flags_results_;

	vector<int> selectedBits_;
	vector<int> results_;
	//int HBHE;

};

// Constructor
NtupleFilter::NtupleFilter(edm::ParameterSet iConfig): 
	Obj2BranchBase(iConfig),
	triggerSelection_(iConfig.getParameter<vector<string> >("filterSelection")),
	src_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("src"))),
	currentrun_(0)
{
	typedef vector<edm::ParameterSet> vpset;
	results_.resize(triggerSelection_.size());
	selectedBits_.resize(triggerSelection_.size());
	for(size_t t = 0 ; t < triggerSelection_.size() ; ++t)
	{
		tree_.branch(prefix_+SEPARATOR+triggerSelection_[t], &(results_[t]), (prefix_+SEPARATOR+triggerSelection_[t]+"/I").c_str()); 
	}

	vpset boolflags = iConfig.getParameter<vpset>("booleans");
	flags_results_.resize(boolflags.size());
	for(size_t i = 0; i < boolflags.size(); ++i) { 
		bool_tokens_.push_back(consumes<bool>(boolflags[i].getParameter<edm::InputTag>("tag")));
		string name = boolflags[i].getParameter<string>("name");
		tree_.branch(prefix_+SEPARATOR+name, &(flags_results_[i]), (prefix_+SEPARATOR+name+"/I").c_str());
	}

	//tree_.branch(prefix_+SEPARATOR+"HBHEnew", &HBHE, (prefix_+SEPARATOR+"HBHEnew/I").c_str()); 
}

// Destructor
NtupleFilter::~NtupleFilter()
{
}

void NtupleFilter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<edm::TriggerResults> triggerBits;
	iEvent.getByToken(src_, triggerBits);

	if(iEvent.id().run() != currentrun_) {
		currentrun_ = iEvent.id().run();
		const edm::TriggerNames& names = iEvent.triggerNames(*triggerBits);		
		for(size_t tr = 0 ; tr < triggerSelection_.size() ; ++tr) {
			selectedBits_[tr] = -1;
			for(size_t tn = 0 ; tn < triggerBits->size() ; ++tn) {
        //cout << names.triggerName(tn) << " " << tn << endl;
				if(names.triggerName(tn).find(triggerSelection_[tr]) != string::npos) {
					selectedBits_[tr] = tn;
					break;
				}
			}
		}				
	}

	for(size_t i = 0 ; i < selectedBits_.size() ; ++i) {
		//cout << i << " " << selectedBits_[i] << " " << triggerBits->accept(selectedBits_[i]) << endl;
		if(selectedBits_[i] == -1) {
			results_[i] = 0;
			continue;
		}
		if(triggerBits->accept(selectedBits_[i])) {
			results_[i] = 1; 
		}
		else {
			results_[i] = -1; 
		}
	}

	for(size_t i = 0; i < bool_tokens_.size(); ++i) {
		edm::Handle<bool> flag;
		iEvent.getByToken(bool_tokens_[i], flag);
		flags_results_[i] = (*flag) ? 1 : -1;
	}
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(NtupleFilter);
