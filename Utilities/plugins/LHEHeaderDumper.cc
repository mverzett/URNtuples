// -*- C++ -*-
//
// Package:    Utilities/LHEHeaderDumper.cc
// Class:      LHEHeaderDumper.cc
// 
/**\class LHEHeaderDumper.cc LHEHeaderDumper.cc.cc URNtuples/LHEHeaderDumper.cc/plugins/LHEHeaderDumper.cc.cc

 Description: Dumps the LHE header of a MC edm file

*/
//
// Original Author:  Mauro Verzetti
//         Created:  2 Nov 2016
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include <string>
#include <iostream>
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
using namespace std;
//
// class declaration
//

class LHEHeaderDumper : public edm::EDAnalyzer {
public:
  explicit LHEHeaderDumper(const edm::ParameterSet&);
  ~LHEHeaderDumper() {}

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override {}
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override {}
  virtual void endJob() override {}

  virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override {}

  // ----------member data ---------------------------
  edm::EDGetTokenT< LHERunInfoProduct > src_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
LHEHeaderDumper::LHEHeaderDumper(const edm::ParameterSet& iConfig):
	src_(consumes<LHERunInfoProduct,edm::InRun>(iConfig.getParameter<edm::InputTag>("src")))
{
}

//
// member functions
//
void LHEHeaderDumper::endRun(edm::Run const& run, edm::EventSetup const&) {
	edm::Handle<LHERunInfoProduct> lheinfo;
	run.getByToken(src_, lheinfo);
	
	for(auto iter=lheinfo->headers_begin(); iter!=lheinfo->headers_end(); ++iter){
		cout << iter->tag();
		std::vector<std::string> lines = iter->lines();
		for(auto& line : iter->lines())
			cout << line;
	}
}

void
LHEHeaderDumper::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
DEFINE_FWK_MODULE(LHEHeaderDumper);
